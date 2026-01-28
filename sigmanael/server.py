"""API server for the Sigmanael personal assistant."""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from sigmanael.core.assistant import PersonalAssistant
from sigmanael.integrations.calendar import CalendarIntegration
from sigmanael.integrations.notes import NotesIntegration

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Sigmanael Personal Assistant API",
    description="API for interacting with the Sigmanael personal assistant chatbot",
    version="0.1.0"
)

# Store assistant instances per user
assistants: Dict[str, PersonalAssistant] = {}


class ChatRequest(BaseModel):
    """Chat request model."""
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    conversation_id: str


class UserSetupRequest(BaseModel):
    """User setup request."""
    user_id: str
    user_name: Optional[str] = None
    enable_calendar: bool = True
    enable_notes: bool = True


def get_or_create_assistant(user_id: str, user_name: Optional[str] = None) -> PersonalAssistant:
    """Get existing assistant or create a new one for user.
    
    Args:
        user_id: User identifier
        user_name: User display name
        
    Returns:
        PersonalAssistant instance
    """
    if user_id not in assistants:
        assistant = PersonalAssistant(user_id=user_id, user_name=user_name)
        assistant.add_integration(CalendarIntegration())
        assistant.add_integration(NotesIntegration())
        assistants[user_id] = assistant
    
    return assistants[user_id]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Sigmanael Personal Assistant API",
        "version": "0.1.0",
        "status": "running"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the personal assistant.
    
    Args:
        request: Chat request with user_id and message
        
    Returns:
        ChatResponse with assistant's reply
    """
    try:
        assistant = get_or_create_assistant(request.user_id)
        
        if not assistant.current_conversation:
            assistant.start_conversation()
        
        response = assistant.chat(request.message, request.context)
        
        return ChatResponse(
            response=response,
            conversation_id=assistant.current_conversation.conversation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/setup")
async def setup_user(request: UserSetupRequest):
    """Setup a user's assistant.
    
    Args:
        request: User setup configuration
        
    Returns:
        Success message
    """
    try:
        assistant = PersonalAssistant(
            user_id=request.user_id,
            user_name=request.user_name
        )
        
        if request.enable_calendar:
            assistant.add_integration(CalendarIntegration())
        
        if request.enable_notes:
            assistant.add_integration(NotesIntegration())
        
        assistants[request.user_id] = assistant
        
        return {
            "status": "success",
            "message": f"Assistant setup complete for {request.user_id}",
            "integrations": list(assistant.integrations.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{user_id}/suggestions")
async def get_suggestions(user_id: str):
    """Get personalized suggestions for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        List of suggestions
    """
    try:
        assistant = get_or_create_assistant(user_id)
        suggestions = assistant.learner.get_suggestions()
        
        return {
            "user_id": user_id,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{user_id}/preferences")
async def get_preferences(user_id: str):
    """Get learned preferences for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        User preferences
    """
    try:
        assistant = get_or_create_assistant(user_id)
        preferences = assistant.learner.get_preferences()
        
        return {
            "user_id": user_id,
            "preferences": preferences
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "active_users": len(assistants)
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting Sigmanael API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
