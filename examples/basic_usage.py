#!/usr/bin/env python3
"""
Basic usage examples for Sigil package.
"""

import os
from pathlib import Path
from sigil import SigilConverter, SVGConfig


def basic_character_conversion():
    """Example: Basic character conversion."""
    print("=== Basic Character Conversion ===")
    
    # Use a font from the fonts directory
    font_path = Path(__file__).parent.parent / "fonts" / "NotoSansSC-Regular.ttf"
    
    if not font_path.exists():
        print(f"Font not found: {font_path}")
        return
    
    # Initialize converter
    converter = SigilConverter(str(font_path))
    converter.initialize()
    
    # Basic configuration
    config = SVGConfig(
        px_height=200,
        fill="#2C3E50"
    )
    
    # Convert single character
    svg_content = converter.convert_single_character("A", config)
    
    # Save to file
    output_path = "basic_A.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"✓ Created {output_path}")


def chinese_character_with_grid():
    """Example: Chinese character with practice grid."""
    print("\n=== Chinese Character with Practice Grid ===")
    
    font_path = Path(__file__).parent.parent / "fonts" / "NotoSansSC-Regular.ttf"
    
    if not font_path.exists():
        print(f"Font not found: {font_path}")
        return
    
    converter = SigilConverter(str(font_path))
    converter.initialize()
    
    # Configuration with Tian grid
    config = SVGConfig(
        px_height=300,
        grid_kind="tian",
        grid_color="#E8E8E8",
        fill="#1A1A1A",
        tian_frac=0.7,
        tian_preserve_aspect=True
    )
    
    # Convert with Pinyin
    svg_content = converter.convert_single_character("中", config, "zhōng")
    
    output_path = "chinese_zhong.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"✓ Created {output_path}")


def multiple_characters():
    """Example: Multiple characters conversion."""
    print("\n=== Multiple Characters ===")
    
    font_path = Path(__file__).parent.parent / "fonts" / "NotoSansSC-Regular.ttf"
    
    if not font_path.exists():
        print(f"Font not found: {font_path}")
        return
    
    converter = SigilConverter(str(font_path))
    converter.initialize()
    
    config = SVGConfig(
        px_height=250,
        grid_kind="square",
        grid_color="#F0F0F0",
        fill="#4A90E2"
    )
    
    characters = ["你", "好", "世", "界"]
    pinyin_tokens = ["nǐ", "hǎo", "shì", "jiè"]
    
    svg_content = converter.convert_multiple_characters(characters, config, pinyin_tokens)
    
    output_path = "hello_world.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print(f"✓ Created {output_path}")


def batch_processing():
    """Example: Batch processing multiple characters."""
    print("\n=== Batch Processing ===")
    
    font_path = Path(__file__).parent.parent / "fonts" / "NotoSansSC-Regular.ttf"
    
    if not font_path.exists():
        print(f"Font not found: {font_path}")
        return
    
    converter = SigilConverter(str(font_path))
    converter.initialize()
    
    config = SVGConfig(
        px_height=200,
        grid_kind="tian",
        fill="#8B4513"
    )
    
    # Create output directory
    output_dir = "batch_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Characters to process
    characters = ["春", "夏", "秋", "冬"]
    pinyin_list = ["chūn", "xià", "qiū", "dōng"]
    
    for char, pinyin in zip(characters, pinyin_list):
        svg_content = converter.convert_single_character(char, config, pinyin)
        
        filename = f"U+{ord(char):04X}_{char}.svg"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        
        print(f"✓ Created {filepath}")


if __name__ == "__main__":
    basic_character_conversion()
    chinese_character_with_grid()
    multiple_characters()
    batch_processing()
    
    print("\n🎉 All examples completed!")
    print("Check the generated SVG files to see the results.")