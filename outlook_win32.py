import datetime
import logging

from win32com import client
from win32com.client import CDispatch

from db import Event, create_event, search_event, update_event

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def get_outlook_client() -> CDispatch:
    outlook = client.Dispatch("Outlook.Application")
    ns = outlook.GetNamespace("MAPI")
    return ns


def get_events_range(
    ns: CDispatch, start: datetime.datetime, end: datetime.datetime
) -> list[Event]:
    calendar = ns.GetDefaultFolder(9).Items
    calendar.IncludeRecurrences = True
    calendar.Sort("[Start]")
    restriction = (
        "[Start] >= '"
        + start.strftime("%m/%d/%Y")
        + "' AND [END] <= '"
        + end.strftime("%m/%d/%Y")
        + "'"
    )
    calendar = calendar.Restrict(restriction)
    events = []
    for appointment in calendar:
        start_time = appointment.Start
        end_time = appointment.End
        subject = appointment.Subject
        location = appointment.Location
        event = {
            "day": start_time.strftime("%A"),
            "start_date": start_time,
            "end_date": end_time,
            "name": subject,
            "link": location,
            "recurring": appointment.IsRecurring,
            "organizer": appointment.Organizer,
            "status": appointment.BusyStatus,
            "outlook_id": appointment.EntryID,
        }
        events.append(Event(**event))

    logging.info(len(events))

    return events


if __name__ == "__main__":
    ns = get_outlook_client()
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)
    events = get_events_range(ns, start, end)
    for event in events:
        if search_event(event.name, event.day):
            logging.info(f"El evento {event.name} ya existe")
            update_event(event)
        else:
            logging.info(f"El evento {event.name} no existe")
            create_event(event)
