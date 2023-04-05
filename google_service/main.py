from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import logging
import datetime

from datetime import datetime, timedelta, timezone
import os


current_path = os.path.dirname(os.path.abspath(__file__))


def get_credentials() -> Credentials:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(f'{current_path}/token.json'):
        creds = Credentials.from_authorized_user_file(f'{current_path}/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{current_path}/credentials-service.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f'{current_path}/token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def create_event(name: str, start: datetime, end: datetime, 
                 description: str = None, location: str = None, reminders: bool = False) -> str:
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    event_data = {
        'summary': name,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'America/Mexico_City',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'America/Mexico_City',
        },
        'reminders': {
            'useDefault': reminders,
        },
    }

    # Creamos el evento en el calendario y obtenemos su ID.
    try:
        created_event = service.events().insert(calendarId='primary', body=event_data).execute()
        event_id = created_event['id']
        print('Evento creado con ID: %s' % (event_id))
        return event_id
    except HttpError as error:
        print('Se ha producido un error al crear el evento: %s' % (error))
