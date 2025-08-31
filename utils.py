#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for parsing, formatting, and text processing.
"""

import re
from typing import List, Optional


class UtilityFunctions:
    """Utility functions for parsing and formatting."""
    
    @staticmethod
    def parse_codepoint(s: str) -> int:
        """
        Parse a codepoint from various formats.
        
        Args:
            s: String representation of codepoint
            
        Returns:
            Integer codepoint
            
        Raises:
            ValueError: If parsing fails
        """
        s = s.strip()
        if not s:
            raise ValueError("Empty character argument.")
            
        if len(s) == 1 and not s.startswith(("U+", "u+", "0x", "0X")) and not s.isdigit():
            return ord(s)
            
        if s.lower().startswith("u+"):
            return int(s[2:], 16)
        if s.lower().startswith("0x"):
            return int(s[2:], 16)
        if re.fullmatch(r"[0-9a-fA-F]+", s) and not re.fullmatch(r"\d+", s):
            return int(s, 16)
        if re.fullmatch(r"\d+", s):
            return int(s, 10)
            
        return ord(s[0])
    
    @staticmethod
    def parse_units_or_percent(spec: Optional[str], ref: float, *, default: float = 0.0) -> float:
        """
        Parse units or percentage specification.
        
        Args:
            spec: Specification string (e.g., "10", "50%")
            ref: Reference value for percentage calculation
            default: Default value if spec is None
            
        Returns:
            Parsed value
        """
        if spec is None:
            return default
            
        s = str(spec).strip()
        if s.endswith("%"):
            return float(s[:-1]) * 0.01 * ref
        return float(s)
    
    @staticmethod
    def split_chars(text: str) -> List[str]:
        """Split text into individual characters."""
        return [c for c in text]

    @staticmethod
    def format_number(n: float, decimals: int = 3) -> str:
        """Format number with specified decimal places, removing trailing zeros."""
        s = f"{n:.{decimals}f}".rstrip("0").rstrip(".")
        return s if s else "0"