# Contributing to Marketing Agent

Thank you for your interest in contributing to Marketing Agent! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or screenshots

### Suggesting Enhancements

We welcome feature suggestions! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Ensure existing functionality still works
   - Test new features thoroughly
   - Check for any errors or warnings

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
   
   Use conventional commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Explain the rationale behind your approach

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Documentation

- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update docstrings when changing function behavior
- Include examples for new features

### Testing

- Test with different website types
- Verify brand DNA extraction accuracy
- Check image generation with various prompts
- Test error handling and edge cases

## 🔧 Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/marketing_agent.git
   cd marketing_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. **Set up API keys**
   Create `api_secrets.py`:
   ```python
   MUAPIAPP_API_KEY = "your_key"
   FAL_KEY = "your_key"
   ```

4. **Test your setup**
   ```bash
   python cli_marketing.py
   ```

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- **Asset editing capabilities** - In-app editing of generated assets
- **Performance optimization** - Faster generation and analysis
- **Error handling** - Better error messages and recovery
- **Testing** - Unit tests and integration tests

### Medium Priority
- **Multi-language support** - Support for non-English brands
- **Template library** - Pre-built campaign templates
- **Export formats** - Additional file format support
- **Documentation** - More examples and tutorials

### Nice to Have
- **Analytics integration** - Track campaign performance
- **Social media scheduling** - Direct posting capabilities
- **Batch processing** - Process multiple campaigns
- **UI improvements** - Better CLI or web interface

## 📝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints
- Prioritize the community's best interests

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unprofessional conduct

## 🐛 Bug Bounty

While we don't have a formal bug bounty program, we greatly appreciate:
- Security vulnerability reports (please report privately)
- Critical bug fixes
- Performance improvements
- Documentation enhancements

## 📞 Getting Help

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security concerns or private matters

## 🙏 Recognition

Contributors will be:
- Listed in the project's contributors
- Mentioned in release notes for significant contributions
- Credited in documentation for major features

Thank you for contributing to Marketing Agent! 🚀
