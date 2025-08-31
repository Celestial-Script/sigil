"""
Pytest configuration and fixtures for Sigil tests.
"""

import pytest
import os
from pathlib import Path


@pytest.fixture
def test_font_path():
    """Provide path to test font file."""
    # Use one of the existing fonts in the fonts directory
    font_dir = Path(__file__).parent.parent / "fonts"
    test_font = font_dir / "NotoSansSC-Regular.ttf"
    
    if test_font.exists():
        return str(test_font)
    else:
        pytest.skip("Test font not available")


@pytest.fixture
def sample_characters():
    """Provide sample characters for testing."""
    return ["A", "中", "你", "好"]


@pytest.fixture
def sample_pinyin():
    """Provide sample pinyin for testing."""
    return ["", "zhong1", "ni3", "hao3"]