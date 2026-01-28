"""Main entry point for the Sigmanael personal assistant."""

import os
from dotenv import load_dotenv

from sigmanael.core.assistant import PersonalAssistant
from sigmanael.integrations.calendar import CalendarIntegration
from sigmanael.integrations.notes import NotesIntegration

# Load environment variables
load_dotenv()


def main():
    """Run the personal assistant in interactive mode."""
    # Get user information
    user_id = os.getenv('USER_ID', 'default_user')
    user_name = os.getenv('USER_NAME', 'User')
    
    print("=" * 60)
    print("Welcome to Sigmanael - Your Personal Assistant")
    print("=" * 60)
    print()
    
    # Initialize assistant
    assistant = PersonalAssistant(user_id=user_id, user_name=user_name)
    
    # Add integrations
    print("Setting up integrations...")
    assistant.add_integration(CalendarIntegration())
    assistant.add_integration(NotesIntegration())
    print("✓ Calendar integration enabled")
    print("✓ Notes integration enabled")
    print()
    
    # Start conversation
    assistant.start_conversation()
    
    print(f"Hello {user_name}! I'm Sigmanael, your personal assistant.")
    print("I learn from your behavior and adapt to help you better.")
    print("Type 'help' to see what I can do, or 'quit' to exit.")
    print()
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit command
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAssistant: Goodbye! I'll remember our conversation for next time.")
                break
            
            # Process message and get response
            response = assistant.chat(user_input)
            print(f"\nAssistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nAssistant: Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    main()
