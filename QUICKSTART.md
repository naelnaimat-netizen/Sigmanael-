# Quick Start Guide

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/naelnaimat-netizen/Sigmanael-.git
cd Sigmanael-
```

### 2. Set Up Python Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Your Assistant

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your information
# Set USER_ID, USER_NAME, and other preferences
```

## Running the Assistant

### Interactive Chat Mode

Start the assistant in interactive terminal mode:

```bash
python -m sigmanael.main
```

You'll see:
```
============================================================
Welcome to Sigmanael - Your Personal Assistant
============================================================

Setting up integrations...
✓ Calendar integration enabled
✓ Notes integration enabled

Hello User! I'm Sigmanael, your personal assistant.
I learn from your behavior and adapt to help you better.
Type 'help' to see what I can do, or 'quit' to exit.

You: 
```

### API Server Mode

Run as a REST API server:

```bash
python -m sigmanael.server
```

Then access the API at `http://localhost:8000`

API Documentation available at `http://localhost:8000/docs`

## Example Usage

### Basic Conversation

```
You: Hello!
Assistant: Hello User! How can I assist you today?

You: What can you do?
Assistant: I'm your personal assistant! I can help you with:

Calendar:
  • View Schedule
  • Add Event
  • Query Events
  • Manage Calendar

Notes:
  • Create Note
  • Search Notes
  • Update Note
  • Manage Notes
...
```

### Using Calendar

```
You: What's on my schedule today?
Assistant: You have no events scheduled.
```

### Using Notes

```
You: Create a note about project ideas
Assistant: I can help you with notes. Let me search for 'project ideas'...
```

## Running Examples

Try the included examples:

```bash
python examples.py
```

This will demonstrate:
- Basic conversation
- Calendar management
- Notes management
- Behavior learning
- Preferences management

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

## Using the API

### Send a Chat Message

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Hello!"
  }'
```

### Get Personalized Suggestions

```bash
curl http://localhost:8000/user/user123/suggestions
```

### Get Learned Preferences

```bash
curl http://localhost:8000/user/user123/preferences
```

## Next Steps

1. **Add More Integrations**: Check `DEVELOPMENT.md` for creating custom integrations
2. **Customize Behavior**: Modify the learning algorithms in `sigmanael/learning/`
3. **Connect Real Services**: Implement actual API connections for Google Calendar, Gmail, etc.
4. **Add Voice Interface**: Integrate speech recognition and text-to-speech
5. **Deploy**: Deploy the API server to production

## Troubleshooting

### Dependencies Not Installing

Make sure you have Python 3.8+ installed:
```bash
python3 --version
```

Upgrade pip:
```bash
pip install --upgrade pip
```

### Permission Errors

The assistant stores data in `~/.sigmanael/`. Make sure this directory is writable:
```bash
mkdir -p ~/.sigmanael
chmod 755 ~/.sigmanael
```

### Import Errors

Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Learn More

- Read `README.md` for an overview
- Check `DEVELOPMENT.md` for technical details
- Explore `examples.py` for code examples
- Review tests in `tests/` for usage patterns

## Getting Help

- Check existing issues on GitHub
- Read the documentation
- Review example code
- Ask questions in discussions

Enjoy using Sigmanael! 🚀
