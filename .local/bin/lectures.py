#!/usr/bin/env python3
"""
===============================================================
 Script: lectures.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Defines Lecture and Lectures abstractions.
   - Lecture: represents a single LaTeX lecture file
   - Lectures: collection of Lecture objects with helpers to
     create new lectures, update master.tex, and compile notes.

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

import re
import subprocess
import locale
from datetime import datetime
from pathlib import Path

from config import get_week, DATE_FORMAT, CURRENT_COURSE_ROOT

# Ensure locale for date formatting (adjust if needed)
try:
    locale.setlocale(locale.LC_TIME, "nl_BE.utf8")
except locale.Error:
    # Fallback if locale not installed
    pass


# -----------------------------
# Filename helpers
# -----------------------------

def number2filename(n: int) -> str:
    """Convert lecture number to standard filename."""
    return f"lec_{n:02d}.tex"


def filename2number(s: str) -> int:
    """Extract lecture number from filename."""
    return int(str(s).replace(".tex", "").replace("lec_", ""))


# -----------------------------
# Lecture object
# -----------------------------

class Lecture:
    def __init__(self, file_path: Path, course):
        """
        Parse metadata from lecture file (number, date, title).
        """
        with file_path.open() as f:
            for line in f:
                lecture_match = re.search(r"lecture\{(.*?)\}\{(.*?)\}\{(.*)\}", line)
                if lecture_match:
                    break

        if not lecture_match:
            raise ValueError(f"No lecture metadata found in {file_path}")

        date_str = lecture_match.group(2)
        date = datetime.strptime(date_str, DATE_FORMAT)
        week = get_week(date)
        title = lecture_match.group(3)

        self.file_path = file_path
        self.date = date
        self.week = week
        self.number = filename2number(file_path.stem)
        self.title = title
        self.course = course

    def edit(self):
        """
        Open lecture file in Vim (server: kulak).
        """
        subprocess.Popen([
            "x-terminal-emulator",
            "-e", "zsh", "-i", "-c",
            f"\\vim --servername kulak --remote-silent {self.file_path}"
        ])

    def __str__(self):
        return f'<Lecture {self.course.info["short"]} {self.number} "{self.title}">'


# -----------------------------
# Lectures collection
# -----------------------------

class Lectures(list):
    def __init__(self, course):
        self.course = course
        self.root = course.path
        self.master_file = self.root / "master.tex"
        super().__init__(self.read_files())

    def read_files(self):
        """
        Load all lecture files in course directory.
        """
        files = self.root.glob("lec_*.tex")
        return sorted((Lecture(f, self.course) for f in files), key=lambda l: l.number)

    # -------------------------
    # Parsing lecture ranges
    # -------------------------

    def parse_lecture_spec(self, string: str) -> int:
        """Resolve keywords like 'last' or 'prev' into a lecture number."""
        if len(self) == 0:
            return 0
        if string.isdigit():
            return int(string)
        if string == "last":
            return self[-1].number
        if string == "prev":
            return self[-1].number - 1
        raise ValueError(f"Invalid lecture spec: {string}")

    def parse_range_string(self, arg: str):
        """
        Parse a range string like 'all', '3-5', 'last', etc.
        Returns list of lecture numbers.
        """
        all_numbers = [lecture.number for lecture in self]
        if "all" in arg:
            return all_numbers
        if "-" in arg:
            start, end = [self.parse_lecture_spec(bit) for bit in arg.split("-")]
            return list(set(all_numbers) & set(range(start, end + 1)))
        return [self.parse_lecture_spec(arg)]

    # -------------------------
    # Master.tex helpers
    # -------------------------

    @staticmethod
    def get_header_footer(filepath: Path):
        """
        Split master.tex into header and footer around lecture inputs.
        """
        part = 0
        header, footer = "", ""
        with filepath.open() as f:
            for line in f:
                if "end lectures" in line:
                    part = 2
                if part == 0:
                    header += line
                if part == 2:
                    footer += line
                if "start lectures" in line:
                    part = 1
        return header, footer

    def update_lectures_in_master(self, r):
        """
        Update master.tex to include given lecture numbers.
        """
        header, footer = self.get_header_footer(self.master_file)
        body = "".join("    " + r"\input{" + number2filename(n) + "}\n" for n in r)
        self.master_file.write_text(header + body + footer)

    # -------------------------
    # Lecture creation
    # -------------------------

    def new_lecture(self):
        """
        Create a new lecture file, update master.tex, return Lecture object.
        """
        new_number = self[-1].number + 1 if len(self) else 1
        new_path = self.root / number2filename(new_number)

        today = datetime.today()
        date = today.strftime(DATE_FORMAT)

        new_path.touch()
        new_path.write_text(f"\\lecture{{{new_number}}}{{{date}}}{{}}\n")

        if new_number == 1:
            self.update_lectures_in_master([1])
        else:
            self.update_lectures_in_master([new_number - 1, new_number])

        self.read_files()
        return Lecture(new_path, self.course)

    # -------------------------
    # Compilation
    # -------------------------

    def compile_master(self) -> int:
        """
        Run latexmk on master.tex. Return exit code.
        """
        result = subprocess.run(
            ["latexmk", "-f", "-interaction=nonstopmode", str(self.master_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(self.root),
        )
        return result.returncode
