"""
Unit tests for Sigil models.
"""

import pytest
from sigil.core.models import GlyphData, FontMetrics, SVGConfig


class TestGlyphData:
    """Test GlyphData model."""
    
    def test_glyph_data_creation(self):
        """Test GlyphData creation with valid data."""
        glyph_data = GlyphData(
            codepoint=65,  # 'A'
            glyph_name="A",
            svg_path="M 100 100 L 200 200",
            advance_width=500.0,
            bounds=(0, 0, 400, 600)
        )
        
        assert glyph_data.codepoint == 65
        assert glyph_data.glyph_name == "A"
        assert glyph_data.svg_path == "M 100 100 L 200 200"
        assert glyph_data.advance_width == 500.0
        assert glyph_data.bounds == (0, 0, 400, 600)


class TestFontMetrics:
    """Test FontMetrics model."""
    
    def test_font_metrics_creation(self):
        """Test FontMetrics creation with valid data."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            line_gap=100
        )
        
        assert metrics.units_per_em == 1000
        assert metrics.ascender == 800
        assert metrics.descender == -200
        assert metrics.line_gap == 100


class TestSVGConfig:
    """Test SVGConfig model."""
    
    def test_svg_config_defaults(self):
        """Test SVGConfig with default values."""
        config = SVGConfig()
        
        assert config.bbox_mode == "tight"
        assert config.margin_units == 0.0
        assert config.fill == "currentColor"
        assert config.grid_kind == "none"
        assert config.pinyin_pos == "top"
    
    def test_svg_config_custom_values(self):
        """Test SVGConfig with custom values."""
        config = SVGConfig(
            bbox_mode="em",
            margin_units=50.0,
            fill="#FF0000",
            grid_kind="tian",
            px_height=300.0
        )
        
        assert config.bbox_mode == "em"
        assert config.margin_units == 50.0
        assert config.fill == "#FF0000"
        assert config.grid_kind == "tian"
        assert config.px_height == 300.0