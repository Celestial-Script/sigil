#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Sigil CLI application.
"""

import sys
from typing import Optional, List

from ..core.converter import SigilConverter
from ..chinese.pinyin_processor import PinyinProcessor
from ..utils.functions import UtilityFunctions
from .handler import CLIHandler


def main(args: Optional[List[str]] = None) -> None:
    """Main entry point for the CLI application."""
    try:
        # Parse command line arguments
        cli_handler = CLIHandler()
        parsed_args = cli_handler.parse_args(args)
        
        # Initialize converter
        converter = SigilConverter(parsed_args.font, parsed_args.index)
        converter.initialize()
        
        # Create configuration
        config = cli_handler.create_config_from_args(parsed_args, converter.font_metrics.units_per_em)
        
        # Determine characters to process
        if parsed_args.char:
            if parsed_args.char.startswith(('U+', 'u+')):
                codepoint = UtilityFunctions.parse_codepoint(parsed_args.char)
                characters = [chr(codepoint)]
            else:
                characters = [parsed_args.char]
        elif parsed_args.text:
            characters = UtilityFunctions.split_chars(parsed_args.text)
        else:
            print("Error: Must specify either --char or --text", file=sys.stderr)
            sys.exit(1)
        
        # Process Pinyin if provided
        pinyin_tokens = []
        if parsed_args.pinyin:
            pinyin_tokens = PinyinProcessor.normalize_pinyin_for_chars(
                parsed_args.pinyin, len(characters)
            )
        
        # Generate SVG
        if len(characters) == 1:
            pinyin = pinyin_tokens[0] if pinyin_tokens else ""
            svg_content = converter.convert_single_character(characters[0], config, pinyin)
        else:
            svg_content = converter.convert_multiple_characters(characters, config, pinyin_tokens)
        
        # Generate output path
        output_path = cli_handler.generate_output_path(characters, parsed_args.output)
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"SVG saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()