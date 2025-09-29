#!/usr/bin/env python3
"""
===============================================================
 Script: countdown.py
 Author: Kris Yotam (aka. khr1st)
 Date:   2025-09-29
 License: MIT License
 Description:
   Hooks into Google Calendar to display upcoming/current lecture
   info. Updates the active course when matching an event.
   Designed for use with polybar or similar status bars.

 Inspiration:
   Adapted and extended from Gilles Castel's lecture note workflow.
===============================================================
"""

import os
import sys
import re
import math
import sched
import time
import pickle
import datetime
import pytz
import http.client as httplib
from dateutil.parser import parse

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from courses import Courses
from config import USERCALENDARID

# Global: list of courses
courses = Courses()


# -----------------------------
# Google Calendar Authentication
# -----------------------------

def authenticate():
    """
    Authenticate with Google Calendar API, return service object.
    Caches token in token.pickle for reuse.
    """
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing credentials")
            creds.refresh(Request())
        else:
            print("Authorizing new credentials")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


# -----------------------------
# Formatting helpers
# -----------------------------

def join(*args):
    return " ".join(str(e) for e in args if e)


def truncate(string, length):
    ellipsis = " ..."
    return string if len(string) < length else string[: length - len(ellipsis)] + ellipsis


def summary(text):
    return truncate(re.sub(r"X[0-9A-Za-z]+", "", text).strip(), 50)


def gray(text):
    return "%{F#999999}" + text + "%{F-}"


def formatdd(begin, end):
    """
    Format a time delta into minutes or hours string.
    """
    minutes = math.ceil((end - begin).seconds / 60)

    if minutes == 1:
        return "1 minuut"
    if minutes < 60:
        return f"{minutes} min"

    hours = math.floor(minutes / 60)
    rest_minutes = minutes % 60

    if hours > 5 or rest_minutes == 0:
        return f"{hours} uur"

    return f"{hours}:{rest_minutes:02d} uur"


def location(text):
    if not text:
        return ""
    match = re.search(r"\((.*)\)", text)
    return f"{gray('in')} {match.group(1)}" if match else ""


# -----------------------------
# Event processing
# -----------------------------

def event_text(events, now):
    """
    Produce status string based on current and next events.
    """
    current = next((e for e in events if e["start"] < now < e["end"]), None)

    if not current:
        nxt = next((e for e in events if now <= e["start"]), None)
        if nxt:
            return join(
                summary(nxt["summary"]),
                gray("over"),
                formatdd(now, nxt["start"]),
                location(nxt["location"]),
            )
        return ""

    nxt = next((e for e in events if e["start"] >= current["end"]), None)
    if not nxt:
        return join(gray("Einde over"), formatdd(now, current["end"]) + "!")

    if current["end"] == nxt["start"]:
        return join(
            gray("Einde over"),
            formatdd(now, current["end"]) + gray("."),
            gray("Hierna"),
            summary(nxt["summary"]),
            location(nxt["location"]),
        )

    return join(
        gray("Einde over"),
        formatdd(now, current["end"]) + gray("."),
        gray("Hierna"),
        summary(nxt["summary"]),
        location(nxt["location"]),
        gray("na een pauze van"),
        formatdd(current["end"], nxt["start"]),
    )


def activate_course(event):
    """
    Match event summary with course title and set current course.
    """
    course = next(
        (c for c in courses if c.info["title"].lower() in event["summary"].lower()),
        None,
    )
    if course:
        courses.current = course


# -----------------------------
# Event fetching
# -----------------------------

def get_events(service, calendar, morning, evening):
    """
    Fetch all events for a given calendar between morning and evening.
    """
    events_result = service.events().list(
        calendarId=calendar,
        timeMin=morning.isoformat(),
        timeMax=evening.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return [
        {
            "summary": e["summary"],
            "location": e.get("location", None),
            "start": parse(e["start"]["dateTime"]),
            "end": parse(e["end"]["dateTime"]),
        }
        for e in events_result.get("items", [])
        if "dateTime" in e["start"]
    ]


# -----------------------------
# Network helper
# -----------------------------

def wait_for_internet_connection(url, timeout=5):
    """
    Block until an internet connection is available.
    """
    while True:
        conn = httplib.HTTPConnection(url, timeout=timeout)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except Exception:
            conn.close()


# -----------------------------
# Main
# -----------------------------

def main():
    scheduler = sched.scheduler(time.time, time.sleep)

    tz = pytz.timezone(os.environ.get("TZ", "Europe/Brussels"))

    service = authenticate()

    now = datetime.datetime.now(tz=tz)
    morning = now.replace(hour=6, minute=0, microsecond=0)
    evening = now.replace(hour=23, minute=59, microsecond=0)

    events = get_events(service, USERCALENDARID, morning, evening)

    DELAY = 60

    def print_message():
        now = datetime.datetime.now(tz=tz)
        print(event_text(events, now))
        if now < evening:
            scheduler.enter(DELAY, 1, print_message)

    for event in events:
        scheduler.enterabs(
            event["start"].timestamp(), 1, activate_course, argument=(event,)
        )

    scheduler.enter(0, 1, print_message)
    scheduler.run()


if __name__ == "__main__":
    os.chdir(sys.path[0])
    print("Waiting for connection...")
    wait_for_internet_connection("www.google.com")
    main()
