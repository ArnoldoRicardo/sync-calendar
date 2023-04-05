from google_service.main import create_event
from datetime import datetime, timedelta, timezone
import logging
import os
from db import get_events_with_out_google_id, update_google_id


logging.basicConfig(level=logging.INFO)


def main():
    events = get_events_with_out_google_id()
    for event in events:
        google_id = create_event(
            name=event.name,
            start=event.start_date,
            end=event.end_date,
            location=event.organizer
        )
        update_google_id(event.id, google_id)


if __name__ == "__main__":
    main()
