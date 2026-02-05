# Contributing to WordCloud Emergence

Thank you for your interest in contributing to WordCloud Emergence! We welcome contributions from the community.

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ (for development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hazelian0619/wordcloud2tester.git
   cd wordcloud2tester
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .[dev]
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Run tests**
   ```bash
   pytest
   ```

## Development Workflow

### 1. Choose an issue
- Check the [Issues](https://github.com/hazelian0619/wordcloud2tester/issues) page
- Comment on the issue to indicate you're working on it

### 2. Create a branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 3. Make changes
- Follow the coding standards (Black, isort, flake8)
- Write tests for new functionality
- Update documentation as needed

### 4. Run quality checks
```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run tests with coverage
pytest --cov=src/

# Type checking
mypy src/
```

### 5. Commit your changes
```bash
git add .
git commit -m "feat: add your feature description"
```

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code refactoring
- `test:` for tests
- `chore:` for maintenance

### 6. Push and create PR
```bash
git push origin your-branch-name
```
Then create a Pull Request on GitHub.

## Coding Standards

### Python
- Follow PEP 8
- Use type hints
- Write docstrings
- Maximum line length: 88 characters (Black default)

### JavaScript
- Use modern ES6+ syntax
- Follow consistent naming conventions
- Add JSDoc comments for functions

### Git
- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Use English for all commit messages and documentation

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/

# Run specific test
pytest tests/test_specific.py

# Run tests in verbose mode
pytest -v
```

### Writing Tests
- Use pytest framework
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Test both positive and negative cases

## Documentation

### Code Documentation
- Add docstrings to all public functions/classes
- Use Google style docstrings
- Include type hints

### Project Documentation
- Update README.md for significant changes
- Update CHANGELOG.md for version changes
- Add examples for new features

## Pull Request Process

1. **Title**: Use conventional commit format
2. **Description**: Clearly describe what the PR does
3. **Checklist**:
   - [ ] Tests pass
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] CHANGELOG updated (if applicable)
4. **Review**: Wait for maintainer review
5. **Merge**: Squash and merge after approval

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors.

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors

## Getting Help

If you need help:
- Check existing issues and documentation
- Ask questions in GitHub Discussions
- Contact maintainers

Thank you for contributing to WordCloud Emergence! 🎉