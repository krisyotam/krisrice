#!/usr/bin/env python3
"""
===============================================================
 Script: rofi.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Wrapper for launching rofi from Python.
   Provides a simple function `rofi(prompt, options, extra_args)`
   that returns (key, index, selected).

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

import subprocess


def rofi(prompt: str, options: list[str], extra_args: list[str] = None):
    """
    Run rofi with a given prompt and list of options.
    Returns a tuple: (exit_code, index, selected_string).

    - prompt: text displayed at the top of rofi
    - options: list of selectable strings
    - extra_args: additional arguments for rofi (e.g. ["-lines", "5"])
    """
    if extra_args is None:
        extra_args = []

    # Launch rofi
    process = subprocess.Popen(
        ["rofi", "-dmenu", "-p", prompt] + extra_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout, _ = process.communicate("\n".join(options))
    selected = stdout.strip()
    index = options.index(selected) if selected in options else -1

    return process.returncode, index, selected
