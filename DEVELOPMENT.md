# Sigmanael Development Guide

## Architecture Overview

Sigmanael is built with a modular architecture that allows for easy extension and customization.

### Core Components

1. **Personal Assistant (`sigmanael/core/`)**: The main chatbot engine
   - Manages conversations
   - Coordinates integrations
   - Handles user profiles

2. **Integrations (`sigmanael/integrations/`)**: Connectors to digital products
   - Base integration class for creating new connectors
   - Calendar integration
   - Notes integration
   - Extensible plugin system

3. **Behavior Learning (`sigmanael/learning/`)**: Adaptation and personalization
   - Tracks user behavior patterns
   - Learns preferences over time
   - Provides personalized suggestions

4. **Data Models (`sigmanael/models/`)**: Data structures
   - User profiles
   - Conversations and messages
   - Behavior data
   - Integration configurations

5. **Utilities (`sigmanael/utils/`)**: Helper functions
   - Configuration management
   - Data persistence
   - File operations

## Creating Custom Integrations

To create a new integration for connecting to a digital product:

### 1. Create Integration File

Create a new file in `sigmanael/integrations/`, e.g., `email.py`:

```python
from typing import Any, Dict, List, Optional
from sigmanael.integrations import BaseIntegration

class EmailIntegration(BaseIntegration):
    """Integration for email management."""
    
    @property
    def name(self) -> str:
        return "email"
    
    def connect(self) -> bool:
        """Connect to email service."""
        # Implement connection logic
        self.enabled = True
        return True
    
    def disconnect(self) -> None:
        """Disconnect from email service."""
        self.enabled = False
    
    def query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Query emails."""
        # Implement query logic
        return []
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities."""
        return ["read_email", "send_email", "search_inbox"]
```

### 2. Register Integration

Add the integration to your assistant:

```python
from sigmanael.core.assistant import PersonalAssistant
from sigmanael.integrations.email import EmailIntegration

assistant = PersonalAssistant(user_id="user123")
assistant.add_integration(EmailIntegration())
```

## Behavior Learning

The behavior learning system tracks user interactions and adapts the assistant's behavior:

### Tracked Patterns

- **Common Queries**: Types of questions frequently asked
- **Preferred Times**: Times of day when user is most active
- **Topic Interests**: Topics the user frequently discusses
- **Interaction Style**: Preferred communication style

### Using Learned Behavior

```python
# Get personalized suggestions
suggestions = assistant.learner.get_suggestions()

# Get learned preferences
preferences = assistant.learner.get_preferences()

# Adapt response style
response = assistant.learner.adapt_response_style(base_response)
```

## Data Storage

All user data is stored locally by default in `~/.sigmanael/`:

- `profile_{user_id}.json`: User profile and preferences
- `behavior_{user_id}.json`: Learned behavior patterns
- `conversations_{user_id}.json`: Conversation history
- `config.json`: Global configuration

## API Server

Run the assistant as a REST API:

```bash
python -m sigmanael.server
```

### Endpoints

- `POST /chat`: Send a message to the assistant
- `POST /setup`: Setup a user's assistant
- `GET /user/{user_id}/suggestions`: Get personalized suggestions
- `GET /user/{user_id}/preferences`: Get learned preferences
- `GET /health`: Health check

### Example API Usage

```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'user_id': 'user123',
    'message': 'What\'s on my schedule today?'
})

print(response.json()['response'])
```

## Testing

Run tests with pytest:

```bash
pytest tests/ -v
```

### Test Coverage

- Core assistant functionality
- Integration behavior
- Behavior learning
- Data persistence

## Configuration

Configure the assistant using environment variables or `.env` file:

```env
USER_ID=my_user_id
USER_NAME=My Name
ASSISTANT_NAME=Sigmanael
OPENAI_API_KEY=sk-... # Optional
```

## Security Considerations

- All credentials stored in config files should be encrypted
- API endpoints should use authentication in production
- User data is private and stored locally
- No data transmitted to third parties without consent

## Extending the System

### Adding New Capabilities

1. Create new integration classes
2. Implement custom behavior learning algorithms
3. Add new data models for specific use cases
4. Create custom response generators

### Integration Examples

- Google Calendar/Gmail
- Slack/Microsoft Teams
- Trello/Asana
- Spotify/Music services
- Smart home devices
- Social media platforms

## Performance Optimization

- Use async operations for I/O-bound tasks
- Cache frequently accessed data
- Implement pagination for large datasets
- Use database for better scalability

## Troubleshooting

### Common Issues

**Import errors**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

**Data not persisting**: Check file permissions for `~/.sigmanael/`

**Integration not working**: Verify connection credentials and API keys

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Future Enhancements

- Voice interface using speech recognition
- Mobile app (iOS/Android)
- Advanced NLP with transformer models
- Multi-device synchronization
- Collaborative features for teams
- Plugin marketplace
