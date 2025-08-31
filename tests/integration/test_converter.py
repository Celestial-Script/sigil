"""
Integration tests for the main converter functionality.
"""

import pytest
from sigil.core.converter import SigilConverter
from sigil.core.models import SVGConfig


class TestSigilConverter:
    """Integration tests for SigilConverter."""
    
    def test_converter_initialization(self, test_font_path):
        """Test converter initialization."""
        converter = SigilConverter(test_font_path)
        converter.initialize()
        
        assert converter.font_metrics is not None
        assert converter.font_metrics.units_per_em > 0
    
    def test_single_character_conversion(self, test_font_path):
        """Test single character conversion."""
        converter = SigilConverter(test_font_path)
        converter.initialize()
        
        config = SVGConfig(px_height=200.0)
        svg_content = converter.convert_single_character("A", config)
        
        assert isinstance(svg_content, str)
        assert "<svg" in svg_content
        assert "</svg>" in svg_content
        assert "viewBox" in svg_content
    
    def test_single_character_with_pinyin(self, test_font_path):
        """Test single character conversion with Pinyin."""
        converter = SigilConverter(test_font_path)
        converter.initialize()
        
        config = SVGConfig(px_height=200.0, pinyin_pos="top")
        svg_content = converter.convert_single_character("中", config, "zhōng")
        
        assert isinstance(svg_content, str)
        assert "<svg" in svg_content
        assert "zhōng" in svg_content
    
    def test_multiple_character_conversion(self, test_font_path):
        """Test multiple character conversion."""
        converter = SigilConverter(test_font_path)
        converter.initialize()
        
        config = SVGConfig(px_height=200.0)
        characters = ["你", "好"]
        pinyin_tokens = ["nǐ", "hǎo"]
        
        svg_content = converter.convert_multiple_characters(characters, config, pinyin_tokens)
        
        assert isinstance(svg_content, str)
        assert "<svg" in svg_content
        assert "</svg>" in svg_content
    
    def test_converter_with_grid(self, test_font_path):
        """Test converter with practice grid."""
        converter = SigilConverter(test_font_path)
        converter.initialize()
        
        config = SVGConfig(
            px_height=300.0,
            grid_kind="tian",
            grid_color="#E0E0E0"
        )
        
        svg_content = converter.convert_single_character("中", config)
        
        assert isinstance(svg_content, str)
        assert "<svg" in svg_content
        assert "stroke" in svg_content  # Grid lines should have stroke
    
    def test_converter_error_handling(self, test_font_path):
        """Test converter error handling."""
        converter = SigilConverter(test_font_path)
        
        # Should raise error if not initialized
        config = SVGConfig()
        with pytest.raises(RuntimeError, match="not initialized"):
            converter.convert_single_character("A", config)