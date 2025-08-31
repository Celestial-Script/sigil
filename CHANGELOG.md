# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-31

### Added
- Initial release of Sigil package
- Modular font to SVG conversion system
- Support for Chinese practice grids (田字格, 米字格)
- Pinyin annotation with automatic tone mark conversion
- Command-line interface for quick conversions
- Comprehensive Python API for programmatic usage
- Type hints throughout the codebase
- Extensive test suite with unit and integration tests
- Documentation and usage examples
- Support for pip installation

### Features
- **Core Functionality**
  - Font glyph extraction and SVG generation
  - Multiple bounding box modes (tight, em)
  - Configurable margins and sizing
  - Custom fill and stroke styling

- **Chinese Language Support**
  - Traditional practice grid generation
  - Pinyin processing with tone number to tone mark conversion
  - Support for educational character display

- **CLI Interface**
  - Single character conversion
  - Multiple character processing
  - Grid and styling options
  - Flexible output path generation

- **Package Structure**
  - Standard Python package layout with src/ structure
  - Modular architecture with clear separation of concerns
  - Proper __init__.py files with public API
  - Entry points for CLI usage

### Technical Details
- Python 3.8+ support
- Dependencies: fonttools, lxml
- Development tools: pytest, black, flake8, mypy
- Modern packaging with pyproject.toml
- Type safety with comprehensive type hints

### Documentation
- Comprehensive README with usage examples
- API documentation for all public interfaces
- Example scripts demonstrating common use cases
- Development setup and contribution guidelines

## [Unreleased]

### Planned
- Additional grid types and customization options
- Enhanced Pinyin processing features
- Performance optimizations
- Extended font format support
- Web-based demo interface