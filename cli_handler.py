#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface handling and argument parsing.
"""

import argparse
from typing import List, Optional

from models import SVGConfig
from utils import UtilityFunctions


class CLIHandler:
    """Handles command-line interface and argument parsing."""
    
    def __init__(self):
        """Initialize CLI handler."""
        self._parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            prog="glyph2svg",
            description="Export characters from a font to SVG, with optional Chinese grids and Pinyin.",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        
        parser.add_argument("-f", "--font", required=True, help="Path to .ttf/.otf/.ttc/.otc font file.")
        
        g = parser.add_mutually_exclusive_group(required=True)
        g.add_argument("-c", "--char", help="Single character or code point (A, 中, U+4E2D, 0x4E2D, 20013).")
        g.add_argument("-t", "--text", help="One or more literal characters (e.g., '示例').")
        
        parser.add_argument("-o", "--output", help="Output SVG filepath (default: derived from input).")
        parser.add_argument("--index", type=int, default=0, help="Face index for .ttc/.otc (default: 0).")
        
        parser.add_argument("--bbox", choices=["tight", "em"], default="tight",
                            help="Bounding box for single-char mode. With grids/multi-chars, em-sized cells are used.")
        parser.add_argument("--margin", default="2%", help="Outer margin in units or %% of UPM.")
        parser.add_argument("--px-size", type=float, help="Set SVG height in pixels; width autoscaled.")
        parser.add_argument("--fill", default="currentColor", help="Glyph fill color.")
        parser.add_argument("--stroke", help="Glyph stroke color.")
        parser.add_argument("--stroke-width", type=float, help="Glyph stroke width in px.")
        
        parser.add_argument("--grid", choices=["none", "square", "fang", "tian", "mi"], default="none",
                            help="Practice grid: square(=fang), tian(田字格), mi(米字格).")
        parser.add_argument("--grid-color", default="#888", help="Grid stroke color.")
        parser.add_argument("--grid-border-width", default="1.2%", help="Outer border stroke width (units or %% of cell).")
        parser.add_argument("--grid-guide-width", default="0.6%", help="Guide line stroke width (units or %% of cell).")
        parser.add_argument("--grid-dash", default="4,6", help="Dash pattern for guide lines (empty for solid).")
        parser.add_argument("--cell-size", default=None, help="Cell size in units or %% of UPM (default: 100%% of UPM).")
        
        parser.add_argument("--pinyin", help="Hanyu Pinyin (tone numbers auto-converted, e.g., 'shi4 li4').")
        parser.add_argument("--pinyin-pos", choices=["top", "bottom"], default="top", help="Pinyin position.")
        parser.add_argument("--pinyin-font", help="CSS font-family for Pinyin.")
        parser.add_argument("--pinyin-size", default="18%", help="Pinyin font-size (units or %% of cell).")
        parser.add_argument("--pinyin-gap", default="6%", help="Gap between Pinyin and grid (units or %% of cell).")
        
        parser.add_argument("--tian-frac", type=float, default=2/3,
                            help="Fraction of the cell to occupy along each axis in 田字格 (default: 0.6667).")
        parser.add_argument("--tian-preserve-aspect", action="store_true",
                            help="Keep uniform scaling in 田字格; the larger dimension becomes tian-frac of the cell, the other <= tian-frac.")
        
        return parser
    
    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """Parse command-line arguments."""
        return self._parser.parse_args(args)
    
    def create_config_from_args(self, args: argparse.Namespace, upm: int) -> SVGConfig:
        """
        Create SVGConfig from parsed arguments.
        
        Args:
            args: Parsed arguments
            upm: Units per em from font
            
        Returns:
            SVG configuration object
        """
        grid_kind = "square" if args.grid == "fang" else args.grid
        
        margin_units = UtilityFunctions.parse_units_or_percent(args.margin, upm)
        cell_units = UtilityFunctions.parse_units_or_percent(args.cell_size, upm, default=upm) if args.cell_size else upm
        grid_border_w = UtilityFunctions.parse_units_or_percent(args.grid_border_width, cell_units)
        grid_guide_w = UtilityFunctions.parse_units_or_percent(args.grid_guide_width, cell_units)
        grid_dash = args.grid_dash.strip() if args.grid_dash else None
        pinyin_size_units = UtilityFunctions.parse_units_or_percent(args.pinyin_size, cell_units)
        pinyin_gap_units = UtilityFunctions.parse_units_or_percent(args.pinyin_gap, cell_units)
        
        return SVGConfig(
            bbox_mode=args.bbox,
            margin_units=margin_units,
            px_height=args.px_size,
            fill=args.fill,
            stroke=args.stroke,
            stroke_width_px=args.stroke_width,
            grid_kind=grid_kind,
            grid_color=args.grid_color,
            grid_border_width=grid_border_w,
            grid_guide_width=grid_guide_w,
            grid_dash=grid_dash,
            cell_units=cell_units,
            pinyin_pos=args.pinyin_pos,
            pinyin_font=args.pinyin_font,
            pinyin_size_units=pinyin_size_units,
            pinyin_gap_units=pinyin_gap_units,
            tian_frac=args.tian_frac,
            tian_preserve_aspect=args.tian_preserve_aspect,
        )
    
    def generate_output_path(self, chars: List[str], output_arg: Optional[str]) -> str:
        """Generate output file path."""
        if output_arg:
            return output_arg
            
        if len(chars) == 1:
            return f"U+{ord(chars[0]):04X}.svg"
        else:
            return "-".join(f"U+{ord(c):04X}" for c in chars) + ".svg"