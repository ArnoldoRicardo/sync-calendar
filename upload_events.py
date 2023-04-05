from google.main import create_event
from datetime import datetime, timedelta, timezone
import logging
import os
from db import get_events_with_out_google_id, update_google_id


logging.basicConfig(level=logging.INFO)


def main():
    events = get_events_with_out_google_id()
    for event in events:
        start = datetime.strptime(event.day + " " + event.startHour, "%Y-%m-%d %H:%M")
        end = datetime.strptime(event.day + " " + event.endHour, "%Y-%m-%d %H:%M")
        google_id = create_event(event.name, start, end)
        update_google_id(event, google_id)


if __name__ == "__main__":
    main()
