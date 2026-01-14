# Contributing to MedGemma HealthConnect

Thank you for your interest in contributing to MedGemma HealthConnect! This document provides guidelines for contributing to the project.

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on patient privacy and safety
- Provide constructive feedback
- Accept constructive criticism gracefully
- Prioritize security and privacy

## How to Contribute

### Reporting Bugs

**Before submitting a bug report:**
- Check existing issues to avoid duplicates
- Collect relevant system information
- Prepare steps to reproduce the issue

**Bug Report Template:**
```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10]
- Browser: [e.g., Chrome 120]

**Privacy Impact:**
Does this affect patient data privacy? [Yes/No]
If yes, describe the impact.
```

### Suggesting Features

**Feature Request Template:**
```markdown
**Feature Description:**
Clear description of the proposed feature

**Use Case:**
Who would benefit and how?

**Privacy Considerations:**
How does this affect patient privacy?

**Implementation Ideas:**
Any thoughts on implementation?
```

### Pull Requests

#### Development Process

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/medgemma-healthconnect.git
   cd medgemma-healthconnect
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Make Your Changes**
   - Follow the coding standards (see below)
   - Add tests for new features
   - Update documentation

5. **Test Your Changes**
   ```bash
   # Run structure tests
   python tests/test_structure.py
   
   # Test the application
   streamlit run app.py
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

7. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

#### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Security fix

## Privacy Impact
- [ ] No impact on privacy
- [ ] Improves privacy
- [ ] Requires privacy review

## Testing
- [ ] Structure tests pass
- [ ] Manual testing completed
- [ ] Edge cases considered

## Checklist
- [ ] Code follows project style
- [ ] Comments added where necessary
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No PII in commits
```

## Coding Standards

### Python Style

Follow PEP 8 with these specifics:

```python
# Good: Clear, documented functions
def process_patient_data(transcript: str) -> Dict[str, Any]:
    """
    Process patient transcript into structured data.
    
    Args:
        transcript: Patient's spoken or written statement
        
    Returns:
        Dictionary containing processed data
        
    Privacy:
        All data processed in-memory only
    """
    # Implementation
    pass

# Bad: Unclear, undocumented
def process(t):
    # What does this do?
    pass
```

### Privacy-First Code

**Always:**
```python
# Good: No persistence
def process_audio(audio_data):
    transcript = transcribe(audio_data)
    # audio_data automatically garbage collected
    return transcript

# Good: Session-based
def handle_request(session_id):
    if not privacy_manager.validate_session(session_id):
        return None
    # Process with session
```

**Never:**
```python
# Bad: Storing sensitive data
def save_transcript(transcript):
    with open('transcripts.txt', 'a') as f:
        f.write(transcript)  # DON'T DO THIS

# Bad: Logging PII
logger.info(f"Patient said: {transcript}")  # DON'T DO THIS
```

### Code Documentation

```python
"""
Module docstring explaining purpose.
Privacy considerations should be noted.
"""

class ExampleClass:
    """
    Class description.
    
    Privacy:
        Describe how this class handles sensitive data
    """
    
    def method(self, param: str) -> bool:
        """
        Method description.
        
        Args:
            param: Parameter description
            
        Returns:
            Return value description
            
        Privacy:
            Note if this handles sensitive data
        """
        pass
```

## Testing Guidelines

### Writing Tests

```python
def test_privacy_feature():
    """Test that sensitive data is not stored"""
    # Setup
    manager = PrivacyManager()
    
    # Action
    session_id = manager.create_session()
    manager.end_session(session_id)
    
    # Assert
    assert not manager.validate_session(session_id)
```

### Test Coverage

Required for:
- All privacy-critical functions
- Data processing logic
- Session management
- Model interfaces

Optional for:
- UI components
- Configuration loading
- Utility functions

## Documentation Standards

### README Updates

When adding features, update:
- Feature list
- Usage examples
- Configuration options
- Dependencies

### Architecture Documentation

For significant changes, update:
- `ARCHITECTURE.md` - System design
- `DEPLOYMENT.md` - Deployment options
- `EXAMPLES.md` - Usage examples

### Inline Comments

```python
# Good: Explain why, not what
# Use quantization to reduce memory footprint for edge devices
model = load_model_quantized(bits=4)

# Bad: Obvious comment
# Load the model
model = load_model()
```

## Security Guidelines

### Security Checklist

- [ ] No hardcoded credentials
- [ ] Input validation implemented
- [ ] No SQL injection vectors
- [ ] XSS prevention in UI
- [ ] CSRF protection enabled
- [ ] Dependencies up to date
- [ ] Secrets in .env only
- [ ] No PII in logs

### Dependency Updates

```bash
# Check for security issues
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update requirements.txt
pip freeze > requirements.txt
```

## Privacy Review Checklist

Before submitting PR involving patient data:

- [ ] No data written to disk
- [ ] No data in logs
- [ ] Session expiration works
- [ ] Data cleared on cleanup
- [ ] No PII in error messages
- [ ] No PII in URLs
- [ ] No PII in HTTP headers
- [ ] Memory cleared after use

## Performance Guidelines

### Optimization Priorities

1. **Memory efficiency** - Use quantization
2. **Response time** - Cache when possible
3. **Startup time** - Lazy load models
4. **Resource usage** - Monitor and optimize

### Performance Testing

```python
import time

def test_performance():
    start = time.time()
    # Your code here
    duration = time.time() - start
    assert duration < 5.0, "Too slow"
```

## Release Process

### Version Numbering

Follow Semantic Versioning (SemVer):
- MAJOR.MINOR.PATCH
- Example: 1.2.3

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number bumped
- [ ] Security review completed
- [ ] Privacy review completed
- [ ] Tag created
- [ ] Release notes written

## Getting Help

### Resources

- **Documentation**: Read README, ARCHITECTURE, DEPLOYMENT
- **Examples**: Check EXAMPLES.md
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions
- **Pull Requests**: Code contributions

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Search closed issues
3. Open a new discussion
4. Tag maintainers if urgent

Thank you for contributing to privacy-first healthcare AI! 🏥
