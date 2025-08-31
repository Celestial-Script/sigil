#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main converter orchestrator for 云篆 (sigil) glyph to SVG conversion.
"""

from typing import List, Optional

from font_processor import FontProcessor
from glyph_extractor import GlyphExtractor
from svg_generator import SVGGenerator
from models import FontMetrics, SVGConfig


class SigilConverter:
    """Main orchestrator class for 云篆 (sigil) glyph to SVG conversion."""
    
    def __init__(self, font_path: str, font_index: int = 0):
        """
        Initialize converter with font.
        
        Args:
            font_path: Path to font file
            font_index: Font index for TTC/OTC files
        """
        self._font_processor = FontProcessor(font_path, font_index)
        self._glyph_extractor: Optional[GlyphExtractor] = None
        self._svg_generator: Optional[SVGGenerator] = None
        
    def initialize(self) -> None:
        """Initialize all components."""
        self._font_processor.load_font()
        self._glyph_extractor = GlyphExtractor(self._font_processor)
        
    def convert_single_character(
        self, 
        character: str, 
        config: SVGConfig,
        pinyin: str = ""
    ) -> str:
        """
        Convert a single character to SVG.
        
        Args:
            character: Character to convert
            config: SVG configuration
            pinyin: Pinyin annotation
            
        Returns:
            SVG content as string
        """
        if not self._glyph_extractor:
            raise RuntimeError("Converter not initialized. Call initialize() first.")
            
        self._svg_generator = SVGGenerator(config)
        
        codepoint = ord(character)
        glyph_data = self._glyph_extractor.extract_glyph_data(codepoint)
        
        return self._svg_generator.generate_single_svg(
            glyph_data, 
            self._font_processor.metrics,
            pinyin
        )
    
    def convert_multiple_characters(
        self, 
        characters: List[str], 
        config: SVGConfig,
        pinyin_tokens: List[str]
    ) -> str:
        """
        Convert multiple characters to SVG.
        
        Args:
            characters: List of characters to convert
            config: SVG configuration
            pinyin_tokens: List of pinyin tokens
            
        Returns:
            SVG content as string
        """
        if not self._glyph_extractor:
            raise RuntimeError("Converter not initialized. Call initialize() first.")
            
        self._svg_generator = SVGGenerator(config)
        
        glyphs_data = []
        for char in characters:
            codepoint = ord(char)
            glyph_data = self._glyph_extractor.extract_glyph_data(codepoint)
            glyphs_data.append(glyph_data)
        
        return self._svg_generator.generate_row_svg(
            glyphs_data,
            self._font_processor.metrics,
            pinyin_tokens
        )
    
    @property
    def font_metrics(self) -> FontMetrics:
        """Get font metrics."""
        return self._font_processor.metrics