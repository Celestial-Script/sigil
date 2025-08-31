#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font processing and loading functionality for 云篆 (sigil).
"""

import os
from typing import Dict, Optional

from fontTools.ttLib import TTFont

from models import FontMetrics


class FontProcessor:
    """Handles font loading, validation, and metadata extraction."""
    
    def __init__(self, font_path: str, font_index: int = 0):
        """
        Initialize FontProcessor with font file path.
        
        Args:
            font_path: Path to the font file
            font_index: Font index for TTC/OTC files
            
        Raises:
            FileNotFoundError: If font file doesn't exist
            ValueError: If font cannot be loaded
        """
        self._font_path = font_path
        self._font_index = font_index
        self._font: Optional[TTFont] = None
        self._metrics: Optional[FontMetrics] = None
        self._cmap: Optional[Dict[int, str]] = None
        
    def load_font(self) -> None:
        """
        Load the font file and extract basic metrics.
        
        Raises:
            ValueError: If font loading fails
        """
        try:
            self._font = TTFont(self._font_path, fontNumber=self._font_index)
            self._extract_metrics()
            self._cmap = self._font.getBestCmap() or {}
        except Exception as e:
            raise ValueError(f"Failed to load font '{self._font_path}': {e}")
    
    def _extract_metrics(self) -> None:
        """Extract font metrics and metadata."""
        if not self._font:
            raise RuntimeError("Font not loaded")
            
        upm = int(self._font["head"].unitsPerEm)
        
        # Extract font names
        try:
            name_table = self._font["name"]
            family = name_table.getDebugName(1) or ""
            subfamily = name_table.getDebugName(2) or ""
            full_name = name_table.getDebugName(4) or ""
            
            font_name = (
                full_name or 
                (family + (" " + subfamily if subfamily and subfamily.lower() != "regular" else ""))
            ).strip() or os.path.basename(self._font_path)
        except Exception:
            family = subfamily = ""
            font_name = os.path.basename(self._font_path)
            
        self._metrics = FontMetrics(
            units_per_em=upm,
            font_name=font_name,
            family_name=family,
            subfamily_name=subfamily
        )
    
    @property
    def font(self) -> TTFont:
        """Get the loaded font object."""
        if not self._font:
            raise RuntimeError("Font not loaded. Call load_font() first.")
        return self._font
    
    @property
    def metrics(self) -> FontMetrics:
        """Get font metrics."""
        if not self._metrics:
            raise RuntimeError("Font not loaded. Call load_font() first.")
        return self._metrics
    
    @property
    def cmap(self) -> Dict[int, str]:
        """Get character map."""
        if self._cmap is None:
            raise RuntimeError("Font not loaded. Call load_font() first.")
        return self._cmap
    
    def get_glyph_name(self, codepoint: int) -> str:
        """
        Get glyph name for a codepoint.
        
        Args:
            codepoint: Unicode codepoint
            
        Returns:
            Glyph name, or .notdef if not found
        """
        return self.cmap.get(codepoint) or self.font.getGlyphName(0)
    
    def has_glyph(self, codepoint: int) -> bool:
        """Check if font has a glyph for the given codepoint."""
        return codepoint in self.cmap