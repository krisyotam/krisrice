#!/usr/bin/env python3
"""
===============================================================
 Script: rofi-courses.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Rofi interface to select and activate a course.
   Highlights the current course, and updates the symlink +
   watch file if a new course is chosen.

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

from rofi import rofi
from courses import Courses


def select_course(courses: Courses):
    """
    Show course list in rofi, return selected index or -1 if cancelled.
    """
    try:
        current_index = courses.index(courses.current)
        args = ["-a", current_index]  # Highlight current course
    except ValueError:
        args = []

    code, index, _ = rofi(
        "Select course",
        [c.info["title"] for c in courses],
        ["-auto-select", "-no-custom", "-lines", str(len(courses))] + args,
    )
    return index


def main():
    courses = Courses()
    index = select_course(courses)

    if index >= 0:
        courses.current = courses[index]
        print(f"[ok] Switched to {courses[index].info['title']}")


if __name__ == "__main__":
    main()
