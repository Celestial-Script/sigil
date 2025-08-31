#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for glyph2svg with backward compatibility.
"""

import sys

from cli_handler import CLIHandler
from converter import Glyph2SVGConverter
from pinyin_processor import PinyinProcessor
from utils import UtilityFunctions


def main() -> None:
    """Main entry point with backward compatibility."""
    cli_handler = CLIHandler()
    args = cli_handler.parse_args()
    
    try:
        # Initialize converter
        converter = Glyph2SVGConverter(args.font, args.index)
        converter.initialize()
        
        # Parse characters
        if args.text:
            chars = UtilityFunctions.split_chars(args.text)
        else:
            cp = UtilityFunctions.parse_codepoint(args.char)
            try:
                chars = [chr(cp)]
            except ValueError:
                print(f"error: invalid code point: U+{cp:04X}", file=sys.stderr)
                sys.exit(2)
        
        # Create configuration
        config = cli_handler.create_config_from_args(args, converter.font_metrics.units_per_em)
        
        # Process pinyin
        pinyin_tokens = PinyinProcessor.normalize_pinyin_for_chars(args.pinyin, len(chars))
        
        # Generate SVG
        if len(chars) == 1 and config.grid_kind == "none" and not args.pinyin:
            svg = converter.convert_single_character(chars[0], config)
        elif len(chars) == 1:
            # Single character with grid or pinyin
            config.bbox_mode = "em"  # Force em mode for grids
            svg = converter.convert_single_character(chars[0], config, pinyin_tokens[0])
        else:
            # Multiple characters
            svg = converter.convert_multiple_characters(chars, config, pinyin_tokens)
        
        # Write output
        output_path = cli_handler.generate_output_path(chars, args.output)
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg)
        except Exception as e:
            print(f"error: failed to write '{output_path}': {e}", file=sys.stderr)
            sys.exit(1)
        
        # Print success message
        font_name = converter.font_metrics.font_name
        if len(chars) == 1:
            print(f"✓ Wrote {output_path}")
            print(f"   font: {font_name} | glyph: {converter._glyph_extractor.extract_glyph_data(ord(chars[0])).name} | codepoint: U+{ord(chars[0]):04X}")
            if config.grid_kind == "tian":
                mode = "uniform" if config.tian_preserve_aspect else "anisotropic"
                print(f"   田字格 fit: {UtilityFunctions.format_number(config.tian_frac)} of cell (mode: {mode}); centered at cross point")
        else:
            print(f"✓ Wrote {output_path}")
            if config.grid_kind == "tian":
                mode = "uniform" if config.tian_preserve_aspect else "anisotropic"
                print(f"   田字格 per cell: {UtilityFunctions.format_number(config.tian_frac)} of cell (mode: {mode}); each centered")
        
        if config.px_height:
            print(f"   pixel height: {config.px_height}px (width auto)")
            
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()