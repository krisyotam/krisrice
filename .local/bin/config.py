#!/usr/bin/env python3
"""
===============================================================
 Script: config.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Global configuration for the LaTeX lecture note system.
   Defines paths, calendar settings, and date formatting.
   Provides helper to compute academic week numbers.

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

from datetime import datetime
from pathlib import Path


# -----------------------------
# Calendar configuration
# -----------------------------

# Default Google Calendar to use for countdown + course events.
# Replace 'primary' with a calendar ID if using a dedicated course calendar.
USERCALENDARID = "primary"


# -----------------------------
# Course symlink and tracking
# -----------------------------

CURRENT_COURSE_SYMLINK = Path("~/current_course").expanduser()
CURRENT_COURSE_ROOT = CURRENT_COURSE_SYMLINK.resolve()
CURRENT_COURSE_WATCH_FILE = Path("/tmp/current_course").resolve()


# -----------------------------
# Root directory for courses
# -----------------------------

ROOT = Path("~/Documents/Kulak/bachelor_3/semester_2").expanduser()


# -----------------------------
# Date formatting
# -----------------------------

DATE_FORMAT = "%a %d %b %Y %H:%M"


# -----------------------------
# Week number utility
# -----------------------------

def get_week(d: datetime = datetime.today()) -> int:
    """
    Compute the academic week number.
    My university labels semester weeks from 1 to 13.
    Adjusted from ISO week numbers using an offset.
    """
    return (int(d.strftime("%W")) + 52 - 5) % 52
