#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinyin processing and tone mark conversion functionality.
"""

import re
import sys
from typing import List, Optional


class PinyinProcessor:
    """Handles Pinyin processing and tone mark conversion."""
    
    # Tone mark mappings
    _TONE_MARKS = {
        "a": "āáǎàa", "e": "ēéěèe", "i": "īíǐìi", 
        "o": "ōóǒòo", "u": "ūúǔùu", "ü": "ǖǘǚǜü",
    }
    
    @classmethod
    def normalize_pinyin_for_chars(cls, pinyin: Optional[str], n_chars: int) -> List[str]:
        """
        Normalize pinyin tokens for the given number of characters.
        
        Args:
            pinyin: Raw pinyin string
            n_chars: Number of characters
            
        Returns:
            List of normalized pinyin tokens
        """
        if not pinyin:
            return [""] * n_chars
            
        tokens = [t for t in re.split(r"[,\s;/|]+", pinyin.strip()) if t]
        tokens = [cls._convert_numbered_to_marked(t) for t in tokens]
        
        if len(tokens) == 1 and n_chars > 1:
            tokens = tokens * n_chars
            
        if len(tokens) != n_chars:
            print(f"warning: pinyin token count ({len(tokens)}) != character count ({n_chars}); trunc/pad applied.", file=sys.stderr)
            tokens = (tokens + [""] * n_chars)[:n_chars]
            
        return tokens
    
    @classmethod
    def _convert_numbered_to_marked(cls, token: str) -> str:
        """Convert numbered pinyin to tone-marked pinyin."""
        match = re.fullmatch(r"([A-Za-züÜ:]+)([0-5])", token)
        if not match:
            return token
            
        base, num = match.group(1), int(match.group(2))
        tone_index = 4 if num in (0, 5) else num - 1
        
        # Normalize ü representations
        normalized = (base.replace("u:", "ü").replace("U:", "Ü")
                          .replace("v", "ü").replace("V", "Ü"))
        lower = normalized.lower()
        
        # Find position for tone mark
        pos = cls._find_tone_mark_position(lower)
        if pos is None:
            return token
            
        target = lower[pos]
        if target not in cls._TONE_MARKS:
            return token
            
        marked_lower = cls._TONE_MARKS[target][tone_index]
        replacement = marked_lower.upper() if normalized[pos].isupper() else marked_lower
        
        return normalized[:pos] + replacement + normalized[pos+1:]
    
    @classmethod
    def _find_tone_mark_position(cls, syllable: str) -> Optional[int]:
        """Find the position where tone mark should be placed."""
        # Tone mark placement rules for Pinyin
        if "a" in syllable:
            return syllable.index("a")
        if "e" in syllable:
            return syllable.index("e")
        if "ou" in syllable:
            return syllable.index("o")
        if "iu" in syllable:
            return syllable.index("u")
        if "ui" in syllable:
            return syllable.index("i")
            
        for vowel in "o i u ü".split():
            if vowel in syllable:
                return syllable.index(vowel)
                
        # Fallback: find any vowel
        for i, char in enumerate(syllable):
            if char in "aeoiuü":
                return i
                
        return None