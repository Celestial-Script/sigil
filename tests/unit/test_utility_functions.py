"""
Unit tests for utility functions.
"""

import pytest
from sigil.utils.functions import UtilityFunctions


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_parse_codepoint_unicode_format(self):
        """Test parsing Unicode format codepoints."""
        assert UtilityFunctions.parse_codepoint("U+0041") == 65
        assert UtilityFunctions.parse_codepoint("u+4e2d") == 20013
        assert UtilityFunctions.parse_codepoint("U+1F600") == 128512
    
    def test_parse_codepoint_hex_format(self):
        """Test parsing hex format codepoints."""
        assert UtilityFunctions.parse_codepoint("0x41") == 65
        assert UtilityFunctions.parse_codepoint("0x4e2d") == 20013
    
    def test_parse_codepoint_decimal(self):
        """Test parsing decimal codepoints."""
        assert UtilityFunctions.parse_codepoint("65") == 65
        assert UtilityFunctions.parse_codepoint("20013") == 20013
    
    def test_parse_codepoint_invalid(self):
        """Test parsing invalid codepoints."""
        with pytest.raises(ValueError):
            UtilityFunctions.parse_codepoint("invalid")
    
    def test_split_chars_ascii(self):
        """Test splitting ASCII characters."""
        result = UtilityFunctions.split_chars("Hello")
        assert result == ["H", "e", "l", "l", "o"]
    
    def test_split_chars_chinese(self):
        """Test splitting Chinese characters."""
        result = UtilityFunctions.split_chars("你好世界")
        assert result == ["你", "好", "世", "界"]
    
    def test_split_chars_mixed(self):
        """Test splitting mixed characters."""
        result = UtilityFunctions.split_chars("Hello世界")
        assert result == ["H", "e", "l", "l", "o", "世", "界"]
    
    def test_parse_units_or_percent_units(self):
        """Test parsing unit values."""
        result = UtilityFunctions.parse_units_or_percent("100", 1000)
        assert result == 100.0
    
    def test_parse_units_or_percent_percentage(self):
        """Test parsing percentage values."""
        result = UtilityFunctions.parse_units_or_percent("10%", 1000)
        assert result == 100.0
    
    def test_parse_units_or_percent_default(self):
        """Test parsing with default value."""
        result = UtilityFunctions.parse_units_or_percent(None, 1000, default=50.0)
        assert result == 50.0
    
    def test_format_number(self):
        """Test number formatting."""
        assert UtilityFunctions.format_number(123.456789) == "123.457"
        assert UtilityFunctions.format_number(123.0) == "123"
        assert UtilityFunctions.format_number(123.456, decimals=2) == "123.46"