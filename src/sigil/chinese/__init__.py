"""
Chinese language processing utilities for Sigil.

This package contains specialized tools for Chinese character processing,
including Pinyin handling and practice grid generation.
"""

from .pinyin_processor import PinyinProcessor

__all__ = [
    'PinyinProcessor',
]