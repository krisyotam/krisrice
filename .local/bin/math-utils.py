#!/usr/bin/env python3
"""
===============================================================
 Script: math-utils.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Shared utility functions for string manipulation and formatting.
   Used across rofi scripts and lecture/course management.

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

# -----------------------------
# Constants
# -----------------------------

MAX_LEN = 40


# -----------------------------
# String helpers
# -----------------------------

def beautify(string: str) -> str:
    """
    Replace underscores/hyphens with spaces and title-case the string.
    Example: "riemann-surfaces" -> "Riemann Surfaces"
    """
    return string.replace("_", " ").replace("-", " ").title()


def unbeautify(string: str) -> str:
    """
    Replace spaces with hyphens and lowercase the string.
    Example: "Riemann Surfaces" -> "riemann-surfaces"
    """
    return string.replace(" ", "-").lower()


def generate_short_title(title: str) -> str:
    """
    Shorten a title for compact display.
    - Truncate to MAX_LEN with ellipsis
    - Remove math dollar signs
    - Provide fallback for empty titles
    """
    short_title = title or "Untitled"
    if len(short_title) >= MAX_LEN:
        short_title = short_title[: MAX_LEN - len(" ... ")] + " ... "
    return short_title.replace("$", "")
