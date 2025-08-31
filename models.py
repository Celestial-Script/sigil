#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data models and configuration classes for glyph2svg.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class GlyphData:
    """Container for glyph information."""
    path: str
    bounds: Optional[Tuple[float, float, float, float]]
    name: str
    codepoint: int
    advance_width: float


@dataclass
class FontMetrics:
    """Container for font metrics and metadata."""
    units_per_em: int
    font_name: str
    family_name: str
    subfamily_name: str


@dataclass
class SVGConfig:
    """Configuration for SVG generation."""
    bbox_mode: str = "tight"
    margin_units: float = 0.0
    px_height: Optional[float] = None
    fill: str = "currentColor"
    stroke: Optional[str] = None
    stroke_width_px: Optional[float] = None
    
    # Grid settings
    grid_kind: str = "none"
    grid_color: str = "#888"
    grid_border_width: float = 0.0
    grid_guide_width: float = 0.0
    grid_dash: Optional[str] = None
    cell_units: float = 1000.0
    
    # Pinyin settings
    pinyin_pos: str = "top"
    pinyin_font: Optional[str] = None
    pinyin_size_units: float = 0.0
    pinyin_gap_units: float = 0.0
    
    # Tian grid settings
    tian_frac: float = 2/3
    tian_preserve_aspect: bool = False