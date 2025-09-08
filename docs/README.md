# Sigil Documentation

Welcome to the comprehensive documentation for Sigil (云篆), a modular Python package for converting font glyphs to SVG format with specialized support for Chinese practice grids and Pinyin annotations.

## Documentation Structure

### 📚 **Core Documentation**

- **[API Reference](API.md)** - Complete API documentation with detailed class and method descriptions
- **[Quick Reference](QUICK_REFERENCE.md)** - Concise reference for common operations
- **[Examples](EXAMPLES.md)** - Comprehensive examples for various use cases
- **[Troubleshooting](TROUBLESHOOTING.md)** - Solutions for common issues and problems

### 🚀 **Getting Started**

1. **Installation**: Follow the installation guide in [API.md](API.md#installation)
2. **Quick Start**: Try the basic examples in [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
3. **Learn by Example**: Explore detailed examples in [EXAMPLES.md](EXAMPLES.md)

### 📖 **Documentation Features**

#### API Reference
- Complete class and method documentation
- Parameter descriptions with types
- Return value specifications
- Usage examples for each component
- Error handling information

#### Quick Reference
- Concise syntax examples
- Common configuration patterns
- CLI command reference
- Performance tips

#### Examples Collection
- Basic character conversion
- Chinese character processing with grids
- Advanced styling techniques
- Batch processing workflows
- Educational applications
- System integration examples
- CLI usage patterns

#### Troubleshooting Guide
- Installation issues
- Font loading problems
- Character conversion errors
- Performance optimization
- Debugging techniques

## Key Features Covered

### 🎯 **Core Functionality**
- Font glyph to SVG conversion
- Multiple bounding box modes
- Custom styling and colors
- Flexible output sizing

### 🇨🇳 **Chinese Language Support**
- Practice grid generation (田字格, 米字格)
- Pinyin annotation with tone marks
- Educational character sheets
- Stroke order practice materials

### 🛠️ **Developer Tools**
- Comprehensive Python API
- Command-line interface
- Batch processing utilities
- Integration examples

### 📱 **Integration Support**
- Web application examples
- Django/Flask integration
- Custom CLI tools
- Thread-safe usage patterns

## Usage Patterns

### For Developers
```python
from sigil import SigilConverter, SVGConfig

converter = SigilConverter("font.ttf")
converter.initialize()

config = SVGConfig(px_height=200, fill="#2C3E50")
svg = converter.convert_single_character("A", config)
```

### For Educators
```python
# Chinese practice sheet
config = SVGConfig(
    px_height=300,
    grid_kind="tian",
    grid_color="#E8E8E8",
    fill="#1A1A1A"
)
svg = converter.convert_single_character("学", config, "xué")
```

### For CLI Users
```bash
sigil -f font.ttf -c 中 --grid tian --pinyin "zhong1" -o practice.svg
```

## Documentation Standards

This documentation follows modern documentation practices:

- **Consistent Formatting**: Standardized code blocks, tables, and examples
- **Complete Coverage**: All public APIs documented with examples
- **Practical Examples**: Real-world usage scenarios
- **Error Handling**: Common issues and solutions
- **Version Information**: Compatibility and requirements

## Contributing to Documentation

To improve this documentation:

1. **Report Issues**: Found unclear sections? Create an issue
2. **Suggest Examples**: Have useful examples? Submit a PR
3. **Fix Errors**: Spotted mistakes? Corrections welcome
4. **Add Languages**: Help translate documentation

## Documentation Maintenance

This documentation is maintained alongside the codebase to ensure:

- **Accuracy**: Examples tested with each release
- **Completeness**: New features documented immediately
- **Clarity**: Regular reviews for readability
- **Relevance**: Outdated information removed promptly

## Quick Navigation

| Need | Go To |
|------|-------|
| Install the package | [API.md#installation](API.md#installation) |
| Basic usage | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| Chinese characters | [EXAMPLES.md#chinese-character-processing](EXAMPLES.md#chinese-character-processing) |
| CLI commands | [QUICK_REFERENCE.md#cli-usage](QUICK_REFERENCE.md#cli-usage) |
| Error solutions | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| Integration help | [EXAMPLES.md#integration-examples](EXAMPLES.md#integration-examples) |
| Performance tips | [TROUBLESHOOTING.md#performance-issues](TROUBLESHOOTING.md#performance-issues) |

## Support Resources

- **GitHub Repository**: [https://github.com/sigil-dev/sigil](https://github.com/sigil-dev/sigil)
- **Issue Tracker**: [https://github.com/sigil-dev/sigil/issues](https://github.com/sigil-dev/sigil/issues)
- **Discussions**: [https://github.com/sigil-dev/sigil/discussions](https://github.com/sigil-dev/sigil/discussions)
- **PyPI Package**: [https://pypi.org/project/sigil/](https://pypi.org/project/sigil/)

---

**Happy coding with Sigil! 🎨**