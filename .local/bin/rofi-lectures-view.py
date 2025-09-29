#!/usr/bin/env python3
"""
===============================================================
 Script: rofi-lectures-view.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Rofi interface to update which lectures are included in
   master.tex for the current course. Lets user quickly select
   between preset lecture ranges and recompiles the notes.

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

from courses import Courses
from rofi import rofi


def select_view():
    """
    Show lecture range options in rofi, return command string.
    """
    commands = ["last", "prev-last", "all", "prev"]
    options = [
        "Current lecture",
        "Last two lectures",
        "All lectures",
        "Previous lectures",
    ]

    _, index, selected = rofi(
        "Select view",
        options,
        ["-lines", "4", "-auto-select"],
    )

    if index >= 0:
        return commands[index]
    return selected


def main():
    lectures = Courses().current.lectures
    command = select_view()
    lecture_range = lectures.parse_range_string(command)
    lectures.update_lectures_in_master(lecture_range)
    lectures.compile_master()
    print(f"[ok] Updated master.tex with {command} lectures")


if __name__ == "__main__":
    main()
