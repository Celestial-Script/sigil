# Sigil (云篆) - Modular Font to SVG Converter

[![PyPI version](https://badge.fury.io/py/sigil.svg)](https://badge.fury.io/py/sigil)
[![Python Support](https://img.shields.io/pypi/pyversions/sigil.svg)](https://pypi.org/project/sigil/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modular, object-oriented Python package for converting font glyphs to SVG format with specialized support for Chinese practice grids and Pinyin annotations.

## Features

- **Font Glyph Processing**: Convert font glyphs to high-quality SVG format
- **Chinese Practice Grids**: Generate structured practice grids (田字格, 米字格) for Chinese character learning
- **Pinyin Annotation Support**: Add Pinyin annotations with automatic tone mark conversion
- **Modular Architecture**: Clean, extensible codebase with clear separation of concerns
- **CLI Interface**: Command-line tool for quick conversions
- **Programmatic API**: Full Python API for integration into applications
- **Type Safety**: Comprehensive type hints throughout the codebase

## Installation

### From PyPI (Recommended)

```bash
pip install sigil
```

### From Source

```bash
git clone https://github.com/sigil-dev/sigil.git
cd sigil
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/sigil-dev/sigil.git
cd sigil
pip install -e ".[dev,test,docs]"
```

## Quick Start

### Command Line Usage

```bash
# Convert a single character
sigil -f /path/to/font.ttf -c A -o letter_A.svg

# Chinese character with practice grid and Pinyin
sigil -f /path/to/font.ttf -c 中 --grid tian --pinyin "zhong1" -o zhong_practice.svg

# Multiple characters
sigil -f /path/to/font.ttf -t "你好" --grid square --pinyin "ni3,hao3" -o hello.svg
```

### Programmatic Usage

```python
from sigil import SigilConverter, SVGConfig

# Initialize converter
converter = SigilConverter("/path/to/font.ttf")
converter.initialize()

# Basic conversion
config = SVGConfig(px_height=200, fill="#2C3E50")
svg_content = converter.convert_single_character("A", config)

# Chinese character with practice grid
config = SVGConfig(
    px_height=300,
    grid_kind="tian",
    grid_color="#E8E8E8",
    fill="#1A1A1A"
)
svg_content = converter.convert_single_character("中", config, "zhōng")

# Save to file
with open("output.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
```

## Package Structure

```
sigil/
├── core/                   # Core font processing modules
│   ├── converter.py        # Main converter orchestrator
│   ├── font_processor.py   # Font loading and metadata
│   ├── glyph_extractor.py  # Glyph data extraction
│   ├── svg_generator.py    # SVG content generation
│   └── models.py          # Data models and configuration
├── chinese/               # Chinese language processing
│   └── pinyin_processor.py # Pinyin handling and tone conversion
├── utils/                 # Utility functions
│   └── functions.py       # Common utility functions
└── cli/                   # Command-line interface
    ├── handler.py         # CLI argument handling
    └── main.py           # CLI entry point
```

## Configuration Options

### SVGConfig Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bbox_mode` | str | "tight" | Bounding box mode: "tight" or "em" |
| `margin_units` | float | 0.0 | Outer margin in font units |
| `px_height` | float | None | SVG height in pixels |
| `fill` | str | "currentColor" | Glyph fill color |
| `stroke` | str | None | Glyph stroke color |
| `stroke_width_px` | float | None | Stroke width in pixels |
| `grid_kind` | str | "none" | Grid type: "none", "square", "tian", "mi" |
| `grid_color` | str | "#888" | Grid line color |
| `pinyin_pos` | str | "top" | Pinyin position: "top" or "bottom" |
| `tian_frac` | float | 2/3 | Fraction of cell occupied in 田字格 |

### Grid Types

- **none**: No grid
- **square**: Simple square grid
- **tian** (田字格): Traditional Chinese practice grid with cross guides
- **mi** (米字格): Advanced practice grid with diagonal guides

## Examples

### Basic Character Conversion

```python
from sigil import SigilConverter, SVGConfig

converter = SigilConverter("font.ttf")
converter.initialize()

config = SVGConfig(px_height=200, fill="#FF6B6B")
svg = converter.convert_single_character("A", config)
```

### Chinese Character Practice Sheet

```python
config = SVGConfig(
    px_height=300,
    grid_kind="tian",
    grid_color="#E0E0E0",
    fill="#2C3E50",
    tian_frac=0.75,
    tian_preserve_aspect=True
)

svg = converter.convert_single_character("学", config, "xué")
```

### Batch Processing

```python
characters = ["春", "夏", "秋", "冬"]
pinyin_list = ["chūn", "xià", "qiū", "dōng"]

for char, pinyin in zip(characters, pinyin_list):
    svg = converter.convert_single_character(char, config, pinyin)
    with open(f"{char}.svg", "w") as f:
        f.write(svg)
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sigil

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
```

## Development

### Setting up Development Environment

```bash
git clone https://github.com/sigil-dev/sigil.git
cd sigil
pip install -e ".[dev]"
```

### Code Quality Tools

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Building the Package

```bash
# Build wheel and source distribution
python -m build

# Install locally
pip install dist/sigil-*.whl
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [fontTools](https://github.com/fonttools/fonttools) for font processing
- Inspired by [traditional Chinese calligraphy practice methods](https://github.com/mengxianghan/xy-character)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Support

- 📖 [Documentation](https://sigil.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/sigil-dev/sigil/issues)
- 💬 [Discussions](https://github.com/sigil-dev/sigil/discussions)
