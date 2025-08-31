"""
Unit tests for Pinyin processor.
"""

import pytest
from sigil.chinese.pinyin_processor import PinyinProcessor


class TestPinyinProcessor:
    """Test PinyinProcessor functionality."""
    
    def test_normalize_pinyin_exact_match(self):
        """Test pinyin normalization with exact character count match."""
        result = PinyinProcessor.normalize_pinyin_for_chars("ni3,hao3", 2)
        assert result == ["nǐ", "hǎo"]
    
    def test_normalize_pinyin_truncate(self):
        """Test pinyin normalization with truncation."""
        result = PinyinProcessor.normalize_pinyin_for_chars("ni3,hao3,shi4", 2)
        assert result == ["nǐ", "hǎo"]
    
    def test_normalize_pinyin_pad(self):
        """Test pinyin normalization with padding."""
        result = PinyinProcessor.normalize_pinyin_for_chars("ni3", 3)
        assert result == ["nǐ", "", ""]
    
    def test_normalize_pinyin_none(self):
        """Test pinyin normalization with None input."""
        result = PinyinProcessor.normalize_pinyin_for_chars(None, 2)
        assert result == ["", ""]
    
    def test_normalize_pinyin_empty(self):
        """Test pinyin normalization with empty input."""
        result = PinyinProcessor.normalize_pinyin_for_chars("", 2)
        assert result == ["", ""]
    
    def test_convert_numbered_to_marked_tone1(self):
        """Test tone 1 conversion."""
        result = PinyinProcessor._convert_numbered_to_marked("ma1")
        assert result == "mā"
    
    def test_convert_numbered_to_marked_tone2(self):
        """Test tone 2 conversion."""
        result = PinyinProcessor._convert_numbered_to_marked("ma2")
        assert result == "má"
    
    def test_convert_numbered_to_marked_tone3(self):
        """Test tone 3 conversion."""
        result = PinyinProcessor._convert_numbered_to_marked("ma3")
        assert result == "mǎ"
    
    def test_convert_numbered_to_marked_tone4(self):
        """Test tone 4 conversion."""
        result = PinyinProcessor._convert_numbered_to_marked("ma4")
        assert result == "mà"
    
    def test_convert_numbered_to_marked_no_tone(self):
        """Test conversion without tone number."""
        result = PinyinProcessor._convert_numbered_to_marked("ma")
        assert result == "ma"
    
    def test_convert_numbered_to_marked_complex(self):
        """Test conversion with complex syllables."""
        result = PinyinProcessor._convert_numbered_to_marked("huang2")
        assert result == "huáng"
        
        result = PinyinProcessor._convert_numbered_to_marked("liang3")
        assert result == "liǎng"
    
    def test_find_tone_mark_position(self):
        """Test finding tone mark position."""
        # Test 'a' priority
        assert PinyinProcessor._find_tone_mark_position("huang") == 2
        
        # Test 'o' priority
        assert PinyinProcessor._find_tone_mark_position("gong") == 1
        
        # Test 'e' priority  
        assert PinyinProcessor._find_tone_mark_position("heng") == 1
        
        # Test 'i' and 'u' together - use second
        assert PinyinProcessor._find_tone_mark_position("liu") == 1
        
        # Test single vowel
        assert PinyinProcessor._find_tone_mark_position("yi") == 1
        
        # Test no vowel
        assert PinyinProcessor._find_tone_mark_position("zh") is None