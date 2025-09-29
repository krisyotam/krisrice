#!/usr/bin/env python3
"""
===============================================================
 Script: courses.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Defines Course and Courses abstractions.
   - Course: represents one LaTeX course (metadata + lectures).
   - Courses: collection of Course objects with support for
     setting the "current" course via symlink and watch file.

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

from pathlib import Path
import yaml

from lectures import Lectures
from config import (
    ROOT,
    CURRENT_COURSE_ROOT,
    CURRENT_COURSE_SYMLINK,
    CURRENT_COURSE_WATCH_FILE,
)


# -----------------------------
# Course object
# -----------------------------

class Course:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem

        # Load metadata from info.yaml
        with (path / "info.yaml").open() as f:
            self.info = yaml.safe_load(f)

        self._lectures = None

    @property
    def lectures(self) -> Lectures:
        """
        Lazily initialize lectures for this course.
        """
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

    def __eq__(self, other) -> bool:
        """
        Courses are equal if their paths match.
        """
        if other is None:
            return False
        return self.path == other.path


# -----------------------------
# Courses collection
# -----------------------------

class Courses(list):
    def __init__(self):
        super().__init__(self.read_files())

    def read_files(self):
        """
        Scan ROOT for course directories and return Course objects.
        """
        course_dirs = [x for x in ROOT.iterdir() if x.is_dir()]
        courses = [Course(path) for path in course_dirs]
        return sorted(courses, key=lambda c: c.name)

    @property
    def current(self) -> Course:
        """
        Return the currently active course.
        """
        return Course(CURRENT_COURSE_ROOT.resolve())

    @current.setter
    def current(self, course: Course):
        """
        Set the current course by updating symlink and watch file.
        """
        if CURRENT_COURSE_SYMLINK.exists() or CURRENT_COURSE_SYMLINK.is_symlink():
            CURRENT_COURSE_SYMLINK.unlink()

        CURRENT_COURSE_SYMLINK.symlink_to(course.path)
        CURRENT_COURSE_WATCH_FILE.write_text(f"{course.info['short']}\n")
