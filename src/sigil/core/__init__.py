"""
Core font processing modules for Sigil.

This package contains the fundamental components for font processing,
glyph extraction, and SVG generation.
"""

from .converter import SigilConverter
from .models import GlyphData, FontMetrics, SVGConfig
from .font_processor import FontProcessor
from .glyph_extractor import GlyphExtractor
from .svg_generator import SVGGenerator

__all__ = [
    'SigilConverter',
    'GlyphData',
    'FontMetrics',
    'SVGConfig', 
    'FontProcessor',
    'GlyphExtractor',
    'SVGGenerator',
]