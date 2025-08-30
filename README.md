# glyph2svg

A Python tool for extracting single Unicode characters from font files and exporting them as standalone SVG files. Perfect for creating practice sheets, logos, or individual character graphics from any font.

## Features

- 🎯 **Single Character Export**: Extract any Unicode character from TTF/OTF/TTC font files
- 📐 **Multiple Layout Modes**: Tight bounding box, em-square, or tian grid (田字格) layouts
- 🎨 **Customizable Styling**: Control fill color, stroke, and dimensions
- 📏 **Flexible Sizing**: Set pixel dimensions or use font units
- 🔤 **Wide Format Support**: Works with .ttf, .otf, .ttc, and .otc font files
- 🌏 **Unicode Support**: Full Unicode support including CJK characters
- 📝 **Practice Grids**: Built-in tian grid (田字格) for Chinese character practice

## Installation

### Prerequisites

- Python 3.7+
- fontTools library

### Install Dependencies

```bash
pip install fonttools
```

### Download

```bash
git clone https://github.com/yourusername/glyph2svg.git
cd glyph2svg
```

## Usage

### Basic Examples

```bash
# Export a Latin character
python glyph2svg.py -f ./Arial.ttf -c A --px-size 512 -o letter_A.svg

# Export a Chinese character with tian grid
python glyph2svg.py -f ./NotoSansSC-Regular.ttf -c 中 --bbox tian --px-size 1024 -o zhong.svg

# Export using Unicode code point
python glyph2svg.py -f ./MyFont.otf -c U+4E2D --px-size 800 -o character.svg

# Export with custom styling
python glyph2svg.py -f ./MyFont.ttf -c 字 --fill "#ff0000" --stroke "#000000" --stroke-width 2 -o red_character.svg
```

### Command Line Options

#### Required Arguments
- `-f, --font`: Path to font file (.ttf/.otf/.ttc/.otc)
- `-c, --char`: Character or code point to export

#### Output Options
- `-o, --output`: Output SVG file path (default: U+XXXX.svg)
- `--px-size`: Set SVG height in pixels (width auto-scaled)

#### Layout Modes
- `--bbox`: Bounding box mode
  - `tight`: Tight bounding box around glyph (default)
  - `em`: Em-square (UPM × UPM) 
  - `tian`: Tian grid (田字格) with character taking 2/3 space, centered

#### Styling Options
- `--fill`: Fill color (default: currentColor)
- `--stroke`: Stroke color
- `--stroke-width`: Stroke width in pixels
- `--margin`: Margin around glyph (font units or percentage, default: 2%)

#### Font Collection Options
- `--index`: Face index for .ttc/.otc files (default: 0)

### Character Input Formats

The tool accepts characters in multiple formats:

| Format | Example | Description |
|--------|---------|-------------|
| Literal | `中` | Direct character input |
| Unicode (U+) | `U+4E2D` | Unicode notation |
| Hexadecimal | `0x4E2D` | Hex with 0x prefix |
| Decimal | `20013` | Decimal code point |

### Layout Modes Explained

#### Tight Mode (`--bbox tight`)
- Crops tightly around the character's actual bounds
- Minimal whitespace
- Best for logos or standalone graphics

#### Em-Square Mode (`--bbox em`)
- Uses the font's em-square (typically 1000×1000 or 2048×2048 units)
- Preserves font's intended spacing
- Good for maintaining consistent character sizing

#### Tian Grid Mode (`--bbox tian`)
- Creates a traditional Chinese practice grid (田字格)
- Character scaled to 2/3 of grid size
- Character centered at grid intersection
- Perfect for Chinese character practice sheets

## Output Format

The generated SVG files include:

- **Scalable Vector Graphics**: Resolution-independent output
- **Metadata**: Font name, glyph name, Unicode code point, and layout info
- **Accessibility**: Proper aria-label attributes
- **Clean Markup**: Optimized SVG structure for web use

### Example Output Structure

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 1040" width="1024" height="1024" aria-label="中">
  <metadata>font=Noto Sans SC Regular; glyph=uni4E2D; codepoint=U+4E2D; unitsPerEm=1000; bboxMode=tian</metadata>
  <!-- Grid lines for tian mode -->
  <rect x="20" y="20" width="1000" height="1000" fill="none" stroke="#ccc" stroke-width="2"/>
  <line x1="520" y1="20" x2="520" y2="1020" stroke="#ccc" stroke-width="1"/>
  <line x1="20" y1="520" x2="1020" y2="520" stroke="#ccc" stroke-width="1"/>
  <!-- Character path -->
  <g transform="translate(186.667 853.333) scale(0.667 -0.667)">
    <path d="M96 661H902V191H825V588H171V186H96Z..." style="fill:currentColor"/>
  </g>
</svg>
```

## Use Cases

### Educational
- **Chinese Character Practice**: Generate practice sheets with tian grids
- **Typography Learning**: Study individual character shapes and proportions
- **Font Analysis**: Compare character designs across different fonts

### Design & Development
- **Logo Creation**: Extract and customize characters for branding
- **Icon Generation**: Create icon sets from symbol fonts
- **Web Graphics**: Generate SVG assets for websites and applications

### Typography & Fonts
- **Glyph Documentation**: Create visual catalogs of font characters
- **Font Testing**: Verify character rendering and bounds
- **Character Comparison**: Compare implementations across font families

## Technical Details

### Coordinate System
- Uses font's native coordinate system (typically Y-up)
- Automatically flips Y-axis for SVG compatibility (Y-down)
- Preserves original font metrics and proportions

### Font Support
- **TrueType (.ttf)**: Full support
- **OpenType (.otf)**: Full support  
- **TrueType Collections (.ttc)**: Supports face selection via --index
- **OpenType Collections (.otc)**: Supports face selection via --index

### Limitations
- Exports vector outlines only (no color layers)
- No text shaping or kerning applied
- Single character export only
- Color emoji fonts won't render color information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/yourusername/glyph2svg.git
cd glyph2svg
pip install fonttools
```

### Running Tests

```bash
# Test with different character types
python glyph2svg.py -f ./test-fonts/NotoSans-Regular.ttf -c A --px-size 512
python glyph2svg.py -f ./test-fonts/NotoSansCJK-Regular.otf -c 中 --bbox tian --px-size 1024
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [fontTools](https://github.com/fonttools/fonttools) - the excellent Python font manipulation library
- Inspired by the need for better Chinese character practice materials
- Thanks to the typography and font development community

## Changelog

### v1.0.0
- Initial release
- Support for TTF/OTF/TTC/OTC fonts
- Tight, em-square, and tian grid layout modes
- Unicode character input support
- SVG output with metadata
- Customizable styling options

---

**Made with ❤️ for typography enthusiasts and language learners**