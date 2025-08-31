# Glyph2SVG - Modular Font to SVG Converter

A modular, object-oriented Python tool for converting font glyphs to SVG format with support for Chinese practice grids and Pinyin annotations.

## Architecture

The codebase has been refactored into a modular structure with clear separation of concerns:

### Core Modules

- **`models.py`** - Data models and configuration classes
  - `GlyphData`: Container for glyph information
  - `FontMetrics`: Font metadata and metrics
  - `SVGConfig`: SVG generation configuration

- **`font_processor.py`** - Font loading and metadata extraction
  - `FontProcessor`: Handles font file loading, validation, and character mapping

- **`glyph_extractor.py`** - Glyph data extraction and transformation
  - `GlyphExtractor`: Extracts SVG paths and bounding boxes from font glyphs

- **`svg_generator.py`** - SVG content generation
  - `SVGGenerator`: Converts glyph data to SVG format with grids and styling

- **`pinyin_processor.py`** - Pinyin processing and tone conversion
  - `PinyinProcessor`: Handles Pinyin normalization and tone mark conversion

- **`converter.py`** - Main orchestrator
  - `Glyph2SVGConverter`: Coordinates the entire conversion pipeline

- **`cli_handler.py`** - Command-line interface
  - `CLIHandler`: Argument parsing and configuration creation

- **`utils.py`** - Utility functions
  - `UtilityFunctions`: Parsing, formatting, and text processing utilities

- **`main.py`** - Entry point with backward compatibility

## Usage Examples

### 1. Basic Character Conversion

**Scenario**: Convert a single English letter to SVG format for web display.

```bash
# Convert letter 'A' from system font
python3 glyph2svg.py -f /System/Library/Fonts/Helvetica.ttc -c A

# Convert using Unicode codepoint
python3 glyph2svg.py -f /System/Library/Fonts/Helvetica.ttc -c U+0041

# Convert with custom styling
python3 glyph2svg.py -f /System/Library/Fonts/Helvetica.ttc -c A \
    --fill "#FF6B6B" --stroke "#4ECDC4" --stroke-width 2 \
    --px-size 200 -o styled_A.svg
```

**Expected Output**: Creates `U+0041.svg` (or `styled_A.svg`) containing the letter 'A' as an SVG with specified styling.

**Explanation**: 
- `-f` specifies the font file path
- `-c` accepts single characters, Unicode notation (U+xxxx), or hex values
- `--fill` and `--stroke` control colors
- `--px-size` sets the output height in pixels
- `-o` specifies custom output filename

### 2. Chinese Character Practice Sheets

**Scenario**: Create practice sheets for Chinese character learning with grid guides and Pinyin pronunciation.

```bash
# Single character with 田字格 (Tian grid) and Pinyin
python3 glyph2svg.py -f /System/Library/Fonts/PingFang.ttc -c 中 \
    --grid tian --pinyin "zhong1" \
    --grid-color "#E0E0E0" --fill "#2C3E50" \
    --px-size 300 -o zhong_practice.svg

# Multiple characters for word practice
python3 glyph2svg.py -f /System/Library/Fonts/PingFang.ttc -t "你好世界" \
    --grid tian --pinyin "ni3,hao3,shi4,jie4" \
    --pinyin-pos top --pinyin-size "20%" \
    --tian-frac 0.7 --tian-preserve-aspect \
    --px-size 400 -o hello_world_practice.svg

# Practice sheet with 米字格 (Mi grid) for detailed stroke guidance
python3 glyph2svg.py -f /System/Library/Fonts/PingFang.ttc -c 龍 \
    --grid mi --pinyin "long2" \
    --grid-border-width "2%" --grid-guide-width "0.8%" \
    --grid-dash "3,3" --fill "#1A1A1A" \
    --px-size 350 -o dragon_practice.svg
```

**Expected Output**: 
- `zhong_practice.svg`: Single character '中' centered in a 田字格 with Pinyin "zhōng" above
- `hello_world_practice.svg`: Four characters in a row, each in its own 田字格 with corresponding Pinyin
- `dragon_practice.svg`: Complex character '龍' in 米字格 with dashed guide lines

**Explanation**:
- `--grid tian/mi` creates Chinese practice grids (田字格/米字格)
- `--pinyin` accepts tone numbers (1-4) which are auto-converted to tone marks
- `--tian-frac` controls how much of the cell the character occupies (default: 2/3)
- `--tian-preserve-aspect` maintains uniform scaling
- `--grid-dash` creates dashed guide lines for better visibility

### 3. Advanced Typography and Design

**Scenario**: Create custom typography elements for graphic design projects with precise control over layout and styling.

```bash
# Logo-style text with tight bounding box
python3 glyph2svg.py -f /System/Library/Fonts/HelveticaNeue.ttc -t "DESIGN" \
    --bbox tight --margin "5%" \
    --fill "url(#gradient)" --stroke "#333" --stroke-width 1.5 \
    --px-size 150 -o design_logo.svg

# Calligraphy-style with custom cell sizing
python3 glyph2svg.py -f /System/Library/Fonts/Brush\ Script\ MT.ttc -t "Script" \
    --bbox em --cell-size "120%" --margin "10%" \
    --fill "#8B4513" --px-size 200 -o script_text.svg

# Technical diagram with precise measurements
python3 glyph2svg.py -f /System/Library/Fonts/Monaco.ttc -c "∑" \
    --bbox em --margin 50 --fill "#2E86AB" \
    --px-size 100 -o sigma_symbol.svg
```

**Expected Output**:
- `design_logo.svg`: Tight-fitted "DESIGN" text suitable for logo use
- `script_text.svg`: Decorative script text with expanded cell spacing
- `sigma_symbol.svg`: Mathematical symbol with precise margins in pixels

**Explanation**:
- `--bbox tight` fits the SVG tightly around the glyph bounds
- `--bbox em` uses the font's em-square for consistent sizing
- `--margin` accepts both percentages and absolute units
- `--cell-size` controls spacing between characters in multi-character output

### 4. Programmatic Usage Examples

**Scenario**: Integrate glyph2svg into Python applications for dynamic SVG generation.

#### Basic Integration
```python
from converter import Glyph2SVGConverter
from models import SVGConfig

# Initialize converter with font
converter = Glyph2SVGConverter("/path/to/font.ttf")
converter.initialize()

# Basic configuration
config = SVGConfig(
    fill="#FF6B6B",
    px_height=200,
    margin_units=20
)

# Convert single character
svg_content = converter.convert_single_character("A", config)

# Save to file
with open("output.svg", "w") as f:
    f.write(svg_content)
```

#### Advanced Configuration
```python
from converter import Glyph2SVGConverter
from models import SVGConfig
from pinyin_processor import PinyinProcessor

# Advanced configuration for Chinese characters
config = SVGConfig(
    bbox_mode="em",
    grid_kind="tian",
    grid_color="#E8E8E8",
    grid_border_width=15.0,
    grid_guide_width=8.0,
    tian_frac=0.75,
    tian_preserve_aspect=True,
    fill="#2C3E50",
    pinyin_pos="top",
    pinyin_size_units=120.0,
    px_height=300
)

# Process multiple characters with Pinyin
converter = Glyph2SVGConverter("NotoSansCJK.ttc")
converter.initialize()

characters = ["学", "习"]
pinyin_raw = "xue2,xi2"
pinyin_tokens = PinyinProcessor.normalize_pinyin_for_chars(pinyin_raw, len(characters))

svg_content = converter.convert_multiple_characters(characters, config, pinyin_tokens)
```

#### Batch Processing
```python
import os
from converter import Glyph2SVGConverter
from models import SVGConfig

def batch_convert_characters(font_path, characters, output_dir):
    """Convert multiple characters to individual SVG files."""
    
    converter = Glyph2SVGConverter(font_path)
    converter.initialize()
    
    config = SVGConfig(
        grid_kind="tian",
        fill="#1A1A1A",
        px_height=250
    )
    
    os.makedirs(output_dir, exist_ok=True)
    
    for char in characters:
        svg = converter.convert_single_character(char, config)
        filename = f"U+{ord(char):04X}_{char}.svg"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg)
        
        print(f"✓ Created {filepath}")

# Usage
chinese_chars = ["春", "夏", "秋", "冬"]
batch_convert_characters("NotoSansCJK.ttc", chinese_chars, "seasons_svg")
```

**Expected Output**: 
- Individual SVG files for each character with consistent styling
- Organized file naming using Unicode codepoints
- Progress feedback during batch processing

**Explanation**:
- Programmatic usage allows dynamic configuration based on application needs
- Batch processing enables efficient generation of multiple SVGs
- The modular structure makes it easy to customize specific components

### 5. Educational Applications

**Scenario**: Create interactive learning materials for language education.

```bash
# Stroke order practice (using grid guides)
python3 glyph2svg.py -f /System/Library/Fonts/PingFang.ttc -c 木 \
    --grid mi --pinyin "mu4" \
    --grid-color "#FFE5B4" --grid-dash "2,4" \
    --fill "none" --stroke "#8B4513" --stroke-width 3 \
    --px-size 400 -o wood_stroke_practice.svg

# Phonetic learning with multiple pronunciation examples
python3 glyph2svg.py -f /System/Library/Fonts/PingFang.ttc -t "妈麻马骂" \
    --grid square --pinyin "ma1,ma2,ma3,ma4" \
    --pinyin-font "Arial" --pinyin-size "15%" \
    --fill "#4A90E2" --px-size 600 -o ma_tones.svg
```

**Expected Output**:
- `wood_stroke_practice.svg`: Character outline with detailed grid for stroke practice
- `ma_tones.svg`: Four characters showing different tones of "ma" with pronunciation guides

**Explanation**:
- `--fill "none" --stroke` creates outline-only characters for tracing
- Different grid types serve different learning purposes
- Consistent Pinyin display helps with pronunciation learning

## Key Features

- **Modular Design**: Each module has a single responsibility
- **Type Safety**: Comprehensive type hints throughout
- **Extensibility**: Easy to add new features without modifying core functionality
- **Backward Compatibility**: Maintains the original script's API and behavior
- **Clean Separation**: Clear boundaries between font processing, glyph extraction, and SVG generation
- **Testability**: Modular structure enables easy unit testing

## Benefits of Modular Structure

1. **Maintainability**: Each module can be updated independently
2. **Reusability**: Components can be used in other projects
3. **Testing**: Individual modules can be tested in isolation
4. **Extensibility**: New features can be added without touching existing code
5. **Readability**: Code is organized by logical functionality
6. **Debugging**: Issues can be isolated to specific modules

The refactored codebase maintains 100% functional compatibility while providing a much more maintainable and extensible foundation for future development.

## Configuration Reference

### SVGConfig Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bbox_mode` | str | "tight" | Bounding box mode: "tight" or "em" |
| `margin_units` | float | 0.0 | Outer margin in font units |
| `px_height` | float | None | SVG height in pixels (width auto-scaled) |
| `fill` | str | "currentColor" | Glyph fill color |
| `stroke` | str | None | Glyph stroke color |
| `stroke_width_px` | float | None | Stroke width in pixels |
| `grid_kind` | str | "none" | Grid type: "none", "square", "tian", "mi" |
| `grid_color` | str | "#888" | Grid line color |
| `grid_border_width` | float | 0.0 | Border thickness |
| `grid_guide_width` | float | 0.0 | Guide line thickness |
| `grid_dash` | str | None | Dash pattern (e.g., "4,6") |
| `cell_units` | float | 1000.0 | Cell size in font units |
| `pinyin_pos` | str | "top" | Pinyin position: "top" or "bottom" |
| `pinyin_font` | str | None | CSS font-family for Pinyin |
| `pinyin_size_units` | float | 0.0 | Pinyin font size |
| `pinyin_gap_units` | float | 0.0 | Gap between Pinyin and grid |
| `tian_frac` | float | 2/3 | Fraction of cell occupied in 田字格 |
| `tian_preserve_aspect` | bool | False | Maintain aspect ratio in 田字格 |

### Command Line Options

#### Font and Character Selection
- `-f, --font`: Font file path (required)
- `-c, --char`: Single character or codepoint
- `-t, --text`: Multiple characters
- `--index`: Font face index for TTC/OTC files

#### Output Control
- `-o, --output`: Output SVG file path
- `--bbox`: Bounding box mode (tight/em)
- `--margin`: Outer margin (units or percentage)
- `--px-size`: SVG height in pixels

#### Styling
- `--fill`: Glyph fill color
- `--stroke`: Glyph stroke color  
- `--stroke-width`: Stroke width in pixels

#### Grid Options
- `--grid`: Grid type (none/square/fang/tian/mi)
- `--grid-color`: Grid line color
- `--grid-border-width`: Border line width
- `--grid-guide-width`: Guide line width
- `--grid-dash`: Dash pattern for guides
- `--cell-size`: Cell size (units or percentage)

#### Pinyin Options
- `--pinyin`: Pinyin text with tone numbers
- `--pinyin-pos`: Position (top/bottom)
- `--pinyin-font`: CSS font family
- `--pinyin-size`: Font size (units or percentage)
- `--pinyin-gap`: Gap from grid (units or percentage)

#### Tian Grid Specific
- `--tian-frac`: Cell occupation fraction
- `--tian-preserve-aspect`: Maintain aspect ratio

## Troubleshooting

### Common Issues

**Font not found error**
```bash
error: Failed to load font '/path/to/font.ttf': [Errno 2] No such file or directory
```
*Solution*: Verify the font file path exists and is accessible.

**Character not in font warning**
```bash
warning: U+4E2D not in font; exporting '.notdef'.
```
*Solution*: Use a font that contains the desired character, or check the character encoding.

**Pinyin token count mismatch**
```bash
warning: pinyin token count (2) != character count (3); trunc/pad applied.
```
*Solution*: Ensure the number of Pinyin syllables matches the number of characters.

**Permission denied when writing output**
```bash
error: failed to write 'output.svg': [Errno 13] Permission denied
```
*Solution*: Check write permissions for the output directory or specify a different output path.

### Performance Tips

1. **Batch Processing**: Use programmatic interface for multiple conversions
2. **Font Caching**: Reuse `Glyph2SVGConverter` instances for the same font
3. **Memory Management**: Call `initialize()` only once per font
4. **Output Optimization**: Use appropriate `px_height` to balance quality and file size

### Best Practices

1. **Font Selection**: Use fonts with good Unicode coverage for international characters
2. **Grid Usage**: Choose appropriate grid types for the target audience
3. **Color Accessibility**: Ensure sufficient contrast for educational materials
4. **File Organization**: Use descriptive filenames for batch-generated SVGs
5. **Version Control**: Keep font files in version control for reproducible builds