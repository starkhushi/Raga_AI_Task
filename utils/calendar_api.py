from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']
DEFAULT_TIMEZONE = "Asia/Kolkata"

class GoogleCalendarAPI:
    def __init__(self, credentials_json_path):
        creds = service_account.Credentials.from_service_account_file(credentials_json_path, scopes=SCOPES)
        self.service = build('calendar', 'v3', credentials=creds)

    def get_available_slots(self, calendar_id, date):
        """
        Simple placeholder. Returns list of slot dicts with start datetimes (ISO) and timezone.
        `date` is a date object.
        """
        # Example fixed slots (you can replace with FreeBusy query)
        slots = []
        # 9:00 and 10:00 local time
        for hour in (9, 10, 11, 14, 15):
            start = datetime.combine(date, datetime.min.time()).replace(hour=hour, minute=0)
            slots.append({
                "start": start.isoformat(),
                "timeZone": DEFAULT_TIMEZONE
            })
        return slots

    def book_slot(self, calendar_id, patient_name, start_datetime, end_datetime, summary_extra=None, location=None, timezone=DEFAULT_TIMEZONE):
        """
        start_datetime, end_datetime: naive datetime objects in local time (Asia/Kolkata).
        We pass dateTime and timeZone separately so Google can interpret correctly.
        """
        # ensure ISO strings for dateTime
        start_iso = start_datetime.isoformat()
        end_iso = end_datetime.isoformat()

        event = {
            "summary": f"Appointment with {patient_name}" + (f" - {summary_extra}" if summary_extra else ""),
            "location": location or "",
            "start": {
                "dateTime": start_iso,
                "timeZone": timezone
            },
            "end": {
                "dateTime": end_iso,
                "timeZone": timezone
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        created = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        return created.get("id")
