# Sigmanael - Personal Assistant Chatbot

A unique personal assistant system that connects to all your digital products and adapts to your behavior.

**Copyright © 2026 NAEL Abdelmajid Yacoub AlNaimat. All Rights Reserved.**

## Overview

Sigmanael is an intelligent personal assistant chatbot that learns from your behavior and integrates with your digital ecosystem. It provides personalized assistance based on your habits, preferences, and usage patterns while operating within ethical and legal boundaries.

## Features

- **Thinking Pattern Adaptation**: Mirrors your thinking style and communication preferences
- **Behavior Learning**: Adapts to your personal habits and preferences over time
- **Multi-Product Integration**: Connects to various digital products (calendar, email, notes, etc.)
- **Personalized Responses**: Provides context-aware assistance based on your profile
- **Ethical & Legal Controls**: Built-in safeguards to ensure responsible operation
- **Extensible Plugin System**: Easy to add new integrations
- **Privacy-Focused**: All data stored locally by default

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/naelnaimat-netizen/Sigmanael-.git
cd Sigmanael-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file with your settings:

```env
# Assistant settings
ASSISTANT_NAME=Sigmanael
USER_NAME=YourName

# Optional: OpenAI API key for advanced features
OPENAI_API_KEY=your_api_key_here
```

### Running the Assistant

```bash
# Start the chatbot
python -m sigmanael.main

# Or run the API server
python -m sigmanael.server
```

## Architecture

```
sigmanael/
├── core/           # Core chatbot engine
├── integrations/   # Product connectors
├── learning/       # Behavior learning modules
├── models/         # Data models
└── utils/          # Utilities
```

## Usage Examples

### Basic Conversation

```python
from sigmanael.core.assistant import PersonalAssistant

assistant = PersonalAssistant(user_id="user123")
response = assistant.chat("What's on my schedule today?")
print(response)
```

### Thinking Pattern Insights

```python
# Get insights about your thinking patterns
insights = assistant.get_thinking_insights()
print(insights['communication_style'])
print(insights['common_topics'])
```

### Ethical Controls

```python
# Enable strict ethical filtering
assistant.enable_ethical_mode(strict=True)

# Enable privacy mode
assistant.enable_privacy_mode(enabled=True)
```

### Adding Integrations

```python
from sigmanael.integrations.calendar import CalendarIntegration

assistant.add_integration(CalendarIntegration())
```

## Integrations

Currently supported integrations:
- Calendar (local/Google Calendar)
- Email (IMAP/SMTP)
- Notes (local storage)

More integrations coming soon!

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Integrations

1. Create a new file in `sigmanael/integrations/`
2. Inherit from `BaseIntegration`
3. Implement required methods
4. Register the integration

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Copyright & Ownership

**Copyright © 2026 NAEL Abdelmajid Yacoub AlNaimat. All Rights Reserved.**

See [COPYRIGHT.md](COPYRIGHT.md) for full copyright and ownership information.

## License

See LICENSE file for details.

## Ethical & Legal Guidelines

This system operates within strict ethical and legal boundaries:
- Privacy protection and user data sovereignty
- Responsible AI with no manipulation
- Legal compliance with data protection regulations
- Content filtering and safety mechanisms

See [ETHICS_AND_LEGAL.md](ETHICS_AND_LEGAL.md) for complete guidelines.

## Privacy & Security

- All personal data is stored locally by default
- API keys and credentials stored securely
- No data transmitted to third parties without explicit consent
- Behavior learning happens on-device

## Roadmap

- [ ] Voice interface
- [ ] Mobile app
- [ ] More third-party integrations
- [ ] Advanced ML models for behavior prediction
- [ ] Multi-device synchronization
- [ ] Team collaboration features