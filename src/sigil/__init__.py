"""
Sigil (云篆) - Modular Font to SVG Converter

A modular, object-oriented Python tool for converting font glyphs to SVG format 
with support for Chinese practice grids and Pinyin annotations.
"""

__version__ = "1.0.0"
__author__ = "Sigil Development Team"
__email__ = "dev@sigil.com"
__description__ = "Modular Font to SVG Converter with Chinese practice grids and Pinyin support"

# Core public API
from .core.converter import SigilConverter
from .core.models import GlyphData, FontMetrics, SVGConfig
from .core.font_processor import FontProcessor
from .core.glyph_extractor import GlyphExtractor
from .core.svg_generator import SVGGenerator

# Chinese processing utilities
from .chinese.pinyin_processor import PinyinProcessor

# Utility functions
from .utils.functions import UtilityFunctions

# CLI interface
from .cli.handler import CLIHandler

__all__ = [
    # Core classes
    'SigilConverter',
    'GlyphData',
    'FontMetrics', 
    'SVGConfig',
    'FontProcessor',
    'GlyphExtractor',
    'SVGGenerator',
    
    # Chinese processing
    'PinyinProcessor',
    
    # Utilities
    'UtilityFunctions',
    
    # CLI
    'CLIHandler',
]