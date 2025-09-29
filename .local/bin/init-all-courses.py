#!/usr/bin/env python3
"""
===============================================================
 Script: init-all-courses.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Initializes LaTeX note-taking course directories by
   creating `master.tex`, `master.tex.latexmain`, and
   ensuring `figures/` exists for each course.

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

from courses import Courses


def build_master_content(course_title: str) -> str:
    """
    Return the LaTeX master.tex skeleton as a single string.
    """
    lines = [
        r'\documentclass[a4paper]{article}',
        r'\input{../preamble.tex}',
        fr'\title{{{course_title}}}',
        r'\begin{document}',
        r'    \maketitle',
        r'    \tableofcontents',
        r'    % start lectures',
        r'    % end lectures',
        r'\end{document}',
    ]
    return '\n'.join(lines)


def init_course(course):
    """
    Initialize one course directory with master.tex,
    .latexmain marker, and figures/ folder.
    """
    lectures = course.lectures
    course_title = lectures.course.info["title"]

    # Write master.tex with minimal skeleton
    lectures.master_file.touch(exist_ok=True)
    lectures.master_file.write_text(build_master_content(course_title))

    # Touch helper file for latexmk integration
    (lectures.root / 'master.tex.latexmain').touch(exist_ok=True)

    # Ensure figures directory exists
    (lectures.root / 'figures').mkdir(exist_ok=True)

    print(f"[ok] Initialized {course_title}")


def main():
    """
    Iterate over all courses and initialize them.
    """
    for course in Courses():
        init_course(course)


if __name__ == "__main__":
    main()
