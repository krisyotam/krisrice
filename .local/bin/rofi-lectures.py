#!/usr/bin/env python3
"""
===============================================================
 Script: rofi-lectures.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Rofi interface to manage lectures in the current course.
   - Select a lecture to edit in Vim
   - Press Ctrl+n to create a new lecture and open it

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

from courses import Courses
from rofi import rofi
from utils import generate_short_title, MAX_LEN


def build_options(lectures):
    """
    Format lecture list for rofi display.
    """
    sorted_lectures = sorted(lectures, key=lambda l: -l.number)
    options = [
        "{number: >2}. <b>{title: <{fill}}</b> <span size='smaller'>{date} ({week})</span>".format(
            fill=MAX_LEN,
            number=lec.number,
            title=generate_short_title(lec.title),
            date=lec.date.strftime("%a %d %b"),
            week=lec.week,
        )
        for lec in sorted_lectures
    ]
    return sorted_lectures, options


def select_lecture(lectures):
    """
    Open rofi, return key and selected lecture index.
    """
    sorted_lectures, options = build_options(lectures)
    key, index, _ = rofi(
        "Select lecture",
        options,
        ["-lines", "5", "-markup-rows", "-kb-row-down", "Down", "-kb-custom-1", "Ctrl+n"],
    )
    return key, index, sorted_lectures


def main():
    lectures = Courses().current.lectures
    key, index, sorted_lectures = select_lecture(lectures)

    if key == 0 and index >= 0:
        sorted_lectures[index].edit()
    elif key == 1:  # Ctrl+n
        new_lecture = lectures.new_lecture()
        new_lecture.edit()


if __name__ == "__main__":
    main()
