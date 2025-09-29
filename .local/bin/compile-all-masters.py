#!/usr/bin/env python3
"""
===============================================================
 Script: compile-all-masters.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Updates each course's master.tex to include all lectures
   and compiles the resulting document. Ensures all notes
   are kept in sync and compiled for quick access (e.g. phone).

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

from courses import Courses


def compile_course(course):
    """
    Update and compile master.tex for one course.
    """
    lectures = course.lectures
    # "all" = include every lecture in this course
    rng = lectures.parse_range_string("all")
    lectures.update_lectures_in_master(rng)
    lectures.compile_master()
    print(f"[ok] Compiled {lectures.course.info['title']}")


def main():
    """
    Iterate over all courses and compile their master files.
    """
    for course in Courses():
        compile_course(course)


if __name__ == "__main__":
    main()
