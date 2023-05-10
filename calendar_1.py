import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_credentials():

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    

    return creds

def create_event(start, end):
    print('attempting to create event')
    credentials = get_credentials()
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': 'Work',
        'location': "Omaha",
        'description': '',
        'start': {
            'dateTime': start,
            'timeZone': 'America/Chicago',
        },
        'end': {
        'dateTime': end,
        'timeZone': 'America/Chicago',
        },
        'reminders': {
            'useDefault': True,
        },
    }

    event = service.events().insert(calendarId='primary', body = event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


