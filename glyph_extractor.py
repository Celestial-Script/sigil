#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Glyph data extraction and transformation functionality for 云篆 (sigil).
"""

import sys
from typing import Optional, Tuple

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

from font_processor import FontProcessor
from models import GlyphData


class GlyphExtractor:
    """Handles glyph data extraction and transformation."""
    
    def __init__(self, font_processor: FontProcessor):
        """
        Initialize GlyphExtractor.
        
        Args:
            font_processor: FontProcessor instance
        """
        self._font_processor = font_processor
    
    def extract_glyph_data(self, codepoint: int) -> GlyphData:
        """
        Extract glyph data for a given codepoint.
        
        Args:
            codepoint: Unicode codepoint
            
        Returns:
            GlyphData object containing path, bounds, and metadata
        """
        glyph_name = self._font_processor.get_glyph_name(codepoint)
        
        if not self._font_processor.has_glyph(codepoint):
            print(f"warning: U+{codepoint:04X} not in font; exporting '.notdef'.", file=sys.stderr)
        
        path, bounds = self._extract_glyph_path_and_bounds(glyph_name)
        advance_width = self._get_advance_width(glyph_name)
        
        return GlyphData(
            path=path,
            bounds=bounds,
            name=glyph_name,
            codepoint=codepoint,
            advance_width=advance_width
        )
    
    def _extract_glyph_path_and_bounds(self, glyph_name: str) -> Tuple[str, Optional[Tuple[float, float, float, float]]]:
        """Extract SVG path and bounding box for a glyph."""
        font = self._font_processor.font
        glyph_set = font.getGlyphSet()
        glyph = glyph_set[glyph_name]
        
        # Extract SVG path
        svg_pen = SVGPathPen(glyph_set)
        glyph.draw(svg_pen)
        path = svg_pen.getCommands()
        
        # Extract bounds
        bounds_pen = BoundsPen(glyph_set)
        glyph.draw(bounds_pen)
        bounds = bounds_pen.bounds
        
        return path, bounds
    
    def _get_advance_width(self, glyph_name: str) -> float:
        """Get advance width for a glyph."""
        try:
            return float(self._font_processor.font["hmtx"].metrics[glyph_name][0])
        except Exception:
            return float(self._font_processor.metrics.units_per_em)