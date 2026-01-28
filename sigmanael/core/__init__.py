"""Core personal assistant chatbot engine."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sigmanael.models import UserProfile, Conversation, Message
from sigmanael.integrations import BaseIntegration
from sigmanael.learning import BehaviorLearner
from sigmanael.utils import get_data_dir, load_json, save_json, sanitize_user_id


class PersonalAssistant:
    """Main personal assistant chatbot class."""
    
    def __init__(self, user_id: str, user_name: Optional[str] = None):
        """Initialize the personal assistant.
        
        Args:
            user_id: Unique user identifier
            user_name: User's display name
        """
        self.user_id = sanitize_user_id(user_id)
        self.user_name = user_name or user_id
        
        # Initialize user profile
        self.profile = self._load_or_create_profile()
        
        # Initialize behavior learner
        self.learner = BehaviorLearner(self.user_id)
        
        # Initialize integrations
        self.integrations: Dict[str, BaseIntegration] = {}
        
        # Initialize conversation
        self.current_conversation: Optional[Conversation] = None
        self.conversation_history_file = get_data_dir() / f"conversations_{self.user_id}.json"
    
    def _load_or_create_profile(self) -> UserProfile:
        """Load existing user profile or create a new one."""
        profile_file = get_data_dir() / f"profile_{self.user_id}.json"
        
        if profile_file.exists():
            data = load_json(profile_file)
            return UserProfile(**data)
        
        profile = UserProfile(
            user_id=self.user_id,
            name=self.user_name
        )
        self._save_profile(profile)
        return profile
    
    def _save_profile(self, profile: UserProfile) -> None:
        """Save user profile to storage."""
        profile_file = get_data_dir() / f"profile_{self.user_id}.json"
        save_json(profile_file, profile.model_dump())
    
    def add_integration(self, integration: BaseIntegration) -> bool:
        """Add a product integration to the assistant.
        
        Args:
            integration: Integration instance to add
            
        Returns:
            bool: True if successfully added and connected
        """
        if integration.connect():
            self.integrations[integration.name] = integration
            return True
        return False
    
    def remove_integration(self, integration_name: str) -> None:
        """Remove a product integration.
        
        Args:
            integration_name: Name of integration to remove
        """
        if integration_name in self.integrations:
            self.integrations[integration_name].disconnect()
            del self.integrations[integration_name]
    
    def start_conversation(self) -> str:
        """Start a new conversation.
        
        Returns:
            Conversation ID
        """
        conversation_id = str(uuid.uuid4())
        self.current_conversation = Conversation(
            conversation_id=conversation_id,
            user_id=self.user_id
        )
        return conversation_id
    
    def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Send a message to the assistant and get a response.
        
        Args:
            message: User's message
            context: Optional context dictionary
            
        Returns:
            Assistant's response
        """
        # Start conversation if needed
        if not self.current_conversation:
            self.start_conversation()
        
        # Record the user message
        self.current_conversation.add_message('user', message)
        
        # Record behavior for learning
        self.learner.record_action('query', {
            'message': message,
            'context': context or {}
        })
        
        # Process the message and generate response
        response = self._process_message(message, context)
        
        # Adapt response based on learned preferences
        response = self.learner.adapt_response_style(response)
        
        # Record the assistant response
        self.current_conversation.add_message('assistant', response)
        
        # Save conversation
        self._save_conversation()
        
        return response
    
    def _process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process user message and generate response.
        
        Args:
            message: User's message
            context: Optional context dictionary
            
        Returns:
            Generated response
        """
        message_lower = message.lower()
        
        # Check if message is related to any integration
        for integration_name, integration in self.integrations.items():
            if self._is_integration_query(message_lower, integration):
                try:
                    result = integration.query(message, context)
                    return self._format_integration_response(integration_name, result)
                except Exception as e:
                    return f"I had trouble accessing your {integration_name}. Error: {str(e)}"
        
        # Handle general queries
        if any(word in message_lower for word in ['help', 'what can you do', 'capabilities']):
            return self._get_capabilities_message()
        
        if any(word in message_lower for word in ['suggest', 'recommendation', 'what should']):
            suggestions = self.learner.get_suggestions(context)
            return "Based on your usage patterns, here are some suggestions:\n" + \
                   "\n".join(f"• {s}" for s in suggestions)
        
        # Default personalized greeting
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return f"Hello {self.user_name}! How can I assist you today?"
        
        # Default response
        return f"I'm here to help, {self.user_name}. " \
               f"You can ask me about your schedule, notes, or other connected services. " \
               f"Say 'help' to see what I can do!"
    
    def _is_integration_query(self, message: str, integration: BaseIntegration) -> bool:
        """Check if message is related to an integration.
        
        Args:
            message: Message text (lowercase)
            integration: Integration instance
            
        Returns:
            bool: True if message relates to this integration
        """
        integration_keywords = {
            'calendar': ['schedule', 'calendar', 'event', 'meeting', 'appointment', 'today', 'tomorrow'],
            'notes': ['note', 'reminder', 'write down', 'remember', 'memo'],
            'email': ['email', 'mail', 'message', 'inbox']
        }
        
        keywords = integration_keywords.get(integration.name, [])
        return any(keyword in message for keyword in keywords)
    
    def _format_integration_response(self, integration_name: str, result: Any) -> str:
        """Format integration query result as response.
        
        Args:
            integration_name: Name of integration
            result: Query result
            
        Returns:
            Formatted response string
        """
        if isinstance(result, list):
            if not result:
                return f"I didn't find anything in your {integration_name}."
            
            if integration_name == 'calendar':
                return self._format_calendar_events(result)
            elif integration_name == 'notes':
                return self._format_notes(result)
        
        return str(result)
    
    def _format_calendar_events(self, events: List[Dict[str, Any]]) -> str:
        """Format calendar events for display."""
        if not events:
            return "You have no events scheduled."
        
        response = f"You have {len(events)} event(s):\n"
        for event in events:
            title = event.get('title', 'Untitled')
            start = event.get('start', 'Unknown time')
            response += f"• {title} at {start}\n"
        return response.strip()
    
    def _format_notes(self, notes: List[Dict[str, Any]]) -> str:
        """Format notes for display."""
        if not notes:
            return "No notes found."
        
        response = f"Found {len(notes)} note(s):\n"
        for note in notes:
            title = note.get('title', 'Untitled')
            response += f"• {title}\n"
        return response.strip()
    
    def _get_capabilities_message(self) -> str:
        """Get message describing assistant capabilities."""
        capabilities = ["I'm your personal assistant! I can help you with:"]
        
        # Add integration capabilities
        for integration in self.integrations.values():
            caps = integration.get_capabilities()
            capabilities.append(f"\n{integration.name.title()}:")
            for cap in caps:
                capabilities.append(f"  • {cap.replace('_', ' ').title()}")
        
        # Add general capabilities
        capabilities.append("\nGeneral:")
        capabilities.append("  • Learn from your behavior patterns")
        capabilities.append("  • Provide personalized suggestions")
        capabilities.append("  • Adapt to your preferences")
        
        return "\n".join(capabilities)
    
    def _save_conversation(self) -> None:
        """Save current conversation to storage."""
        if not self.current_conversation:
            return
        
        # Load existing conversations
        conversations = load_json(self.conversation_history_file)
        if not isinstance(conversations, dict):
            conversations = {}
        
        # Add/update current conversation
        conversations[self.current_conversation.conversation_id] = \
            self.current_conversation.model_dump()
        
        # Save
        save_json(self.conversation_history_file, conversations)
    
    def get_conversation_history(self, limit: int = 10) -> List[Conversation]:
        """Get conversation history.
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversations
        """
        conversations_data = load_json(self.conversation_history_file)
        if not isinstance(conversations_data, dict):
            return []
        
        conversations = [
            Conversation(**data) 
            for data in conversations_data.values()
        ]
        
        # Sort by creation time, most recent first
        conversations.sort(key=lambda c: c.created_at, reverse=True)
        
        return conversations[:limit]
    
    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update user preferences.
        
        Args:
            preferences: Dictionary of preferences to update
        """
        self.profile.preferences.update(preferences)
        self.profile.updated_at = datetime.now()
        self._save_profile(self.profile)
