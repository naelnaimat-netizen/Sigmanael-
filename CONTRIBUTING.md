# Contributing to Sigmanael

Thank you for your interest in contributing to Sigmanael! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain a positive environment

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature suggestions are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style
   - Add tests for new functionality
   - Update documentation

4. **Test your changes**
   ```bash
   pytest tests/ -v
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe what changes you made
   - Reference any related issues
   - Wait for review

## Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/naelnaimat-netizen/Sigmanael-.git
cd Sigmanael-
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Run Tests

```bash
pytest tests/ -v
```

### 3. Run Examples

```bash
python examples.py
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for classes and functions
- Keep functions focused and small
- Use meaningful variable names

### Example

```python
def process_message(message: str, context: Optional[Dict[str, Any]] = None) -> str:
    """Process user message and generate response.
    
    Args:
        message: User's input message
        context: Optional context dictionary
        
    Returns:
        Generated response string
    """
    # Implementation here
    pass
```

## Adding New Integrations

To add a new integration:

1. Create a new file in `sigmanael/integrations/`
2. Inherit from `BaseIntegration`
3. Implement required methods:
   - `name` property
   - `connect()` method
   - `disconnect()` method
   - `query()` method
   - `get_capabilities()` method

4. Add tests in `tests/`
5. Update documentation

### Example Integration

```python
from sigmanael.integrations import BaseIntegration

class MyIntegration(BaseIntegration):
    @property
    def name(self) -> str:
        return "my_integration"
    
    def connect(self) -> bool:
        # Connection logic
        return True
    
    def disconnect(self) -> None:
        # Cleanup
        pass
    
    def query(self, query: str, context: Optional[Dict] = None) -> Any:
        # Query logic
        return result
    
    def get_capabilities(self) -> List[str]:
        return ["capability1", "capability2"]
```

## Testing Guidelines

- Write tests for all new functionality
- Aim for high test coverage
- Use descriptive test names
- Test edge cases and error conditions

### Test Structure

```python
def test_feature_name():
    """Test description."""
    # Arrange
    assistant = PersonalAssistant(user_id="test")
    
    # Act
    result = assistant.some_method()
    
    # Assert
    assert result == expected_value
```

## Documentation

- Update README.md for user-facing changes
- Update DEVELOPMENT.md for technical changes
- Add docstrings to new code
- Include usage examples

## Project Structure

```
sigmanael/
├── core/           # Core functionality
├── integrations/   # Product integrations
├── learning/       # Behavior learning
├── models/         # Data models
├── utils/          # Utilities
├── main.py         # CLI interface
└── server.py       # API server

tests/              # Test suite
examples.py         # Usage examples
```

## Commit Messages

Use clear, descriptive commit messages:

- `Add: new feature description`
- `Fix: bug description`
- `Update: what was updated`
- `Refactor: what was refactored`
- `Docs: documentation changes`
- `Test: test additions or changes`

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions
- Ask in pull request comments

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing to Sigmanael! 🎉
