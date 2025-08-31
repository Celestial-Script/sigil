#!/usr/bin/env python3
"""
CLI entry point for Sigil package.
This script can be used to run the CLI without installing the package.
"""

import sys
import os

# Add src to path for development usage
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sigil.cli.main import main

if __name__ == "__main__":
    main()