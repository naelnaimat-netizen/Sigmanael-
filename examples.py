"""
Example usage of the Sigmanael personal assistant.

This file demonstrates various ways to use the assistant.
"""

from datetime import datetime, timedelta
from sigmanael.core.assistant import PersonalAssistant
from sigmanael.integrations.calendar import CalendarIntegration
from sigmanael.integrations.notes import NotesIntegration


def basic_example():
    """Basic usage example."""
    print("=" * 60)
    print("Basic Example")
    print("=" * 60)
    
    # Create assistant
    assistant = PersonalAssistant(user_id="example_user", user_name="Alex")
    
    # Add integrations
    assistant.add_integration(CalendarIntegration())
    assistant.add_integration(NotesIntegration())
    
    # Start conversation
    assistant.start_conversation()
    
    # Chat with assistant
    print("\nUser: Hello!")
    response = assistant.chat("Hello!")
    print(f"Assistant: {response}\n")
    
    print("User: What can you do?")
    response = assistant.chat("What can you do?")
    print(f"Assistant: {response}\n")


def calendar_example():
    """Calendar integration example."""
    print("=" * 60)
    print("Calendar Example")
    print("=" * 60)
    
    # Create assistant with calendar
    assistant = PersonalAssistant(user_id="calendar_user", user_name="Sarah")
    calendar = CalendarIntegration()
    assistant.add_integration(calendar)
    
    # Add some events
    now = datetime.now()
    calendar.add_event(
        title="Team Meeting",
        start=now.replace(hour=10, minute=0),
        end=now.replace(hour=11, minute=0),
        description="Weekly team sync"
    )
    calendar.add_event(
        title="Lunch with Client",
        start=now.replace(hour=12, minute=30),
        end=now.replace(hour=13, minute=30)
    )
    
    # Query the calendar
    print("\nUser: What's on my schedule today?")
    response = assistant.chat("What's on my schedule today?")
    print(f"Assistant: {response}\n")


def notes_example():
    """Notes integration example."""
    print("=" * 60)
    print("Notes Example")
    print("=" * 60)
    
    # Create assistant with notes
    assistant = PersonalAssistant(user_id="notes_user", user_name="Mike")
    notes = NotesIntegration()
    assistant.add_integration(notes)
    
    # Add some notes
    notes.add_note(
        title="Project Ideas",
        content="1. AI chatbot\n2. Smart calendar\n3. Task manager",
        tags=["ideas", "projects"]
    )
    notes.add_note(
        title="Shopping List",
        content="Milk, eggs, bread, coffee",
        tags=["personal", "shopping"]
    )
    
    # Search notes
    print("\nUser: Find my project notes")
    response = assistant.chat("Find my project notes")
    print(f"Assistant: {response}\n")


def learning_example():
    """Behavior learning example."""
    print("=" * 60)
    print("Learning Example")
    print("=" * 60)
    
    assistant = PersonalAssistant(user_id="learning_user", user_name="Emma")
    assistant.add_integration(CalendarIntegration())
    assistant.add_integration(NotesIntegration())
    
    # Simulate multiple interactions to build behavior patterns
    queries = [
        "What's on my schedule today?",
        "Show me my notes",
        "What's on my calendar?",
        "Any important notes?",
        "What meetings do I have today?"
    ]
    
    print("\nSimulating user interactions to learn behavior...\n")
    for query in queries:
        assistant.chat(query)
    
    # Get learned preferences
    preferences = assistant.learner.get_preferences()
    print("Learned Preferences:")
    print(f"  Common queries: {preferences['common_queries']}")
    print(f"  Topic interests: {preferences['topic_interests']}")
    
    # Get suggestions
    print("\nUser: What should I check?")
    response = assistant.chat("What should I check?")
    print(f"Assistant: {response}\n")


def preferences_example():
    """User preferences example."""
    print("=" * 60)
    print("Preferences Example")
    print("=" * 60)
    
    assistant = PersonalAssistant(user_id="prefs_user", user_name="Jordan")
    
    # Set user preferences
    assistant.update_preferences({
        "timezone": "America/New_York",
        "notification_style": "brief",
        "theme": "dark"
    })
    
    print("\nUser preferences updated:")
    print(f"  {assistant.profile.preferences}")
    print()


def main():
    """Run all examples."""
    basic_example()
    print("\n\n")
    
    calendar_example()
    print("\n\n")
    
    notes_example()
    print("\n\n")
    
    learning_example()
    print("\n\n")
    
    preferences_example()


if __name__ == "__main__":
    main()
