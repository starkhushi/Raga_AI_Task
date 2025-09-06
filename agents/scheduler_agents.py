import random
import string
from datetime import datetime, timedelta

from utils.data_model import SessionLocal, find_patient
from utils.calendar_api import GoogleCalendarAPI
from utils.communication import CommunicationManager
from config import GOOGLE_CREDENTIALS_JSON

class SchedulingState:
    def __init__(self):
        self.patient_info = {}
        self.appointment = {}
        self.is_confirmed = False
        self.confirmation_number = None
        self.errors = []

class SchedulerAgents:
    def __init__(self):
        self.data_session = SessionLocal()
        self.calendar_api = GoogleCalendarAPI(GOOGLE_CREDENTIALS_JSON)
        self.comm_manager = CommunicationManager()
        self.calendar_id = "primary"

    def schedule(self, patient_info, appointment_date, appointment_time, duration_minutes=30, doctor="Dr. Smith", reason=None):
        """
        patient_info: dict with keys first_name,last_name,date_of_birth (date obj or YYYY-MM-DD), phone, email, address, insurance
        appointment_date: date object
        appointment_time: time object
        """
        state = SchedulingState()
        try:
            # lookup or create patient
            p = find_patient(self.data_session, patient_info.get("first_name"), patient_info.get("last_name"), patient_info.get("date_of_birth"))
            if p:
                patient_id = p.patient_id
                is_new = False
            else:
                patient_id = f"P{random.randint(1000,9999)}"
                is_new = True

            state.patient_info = patient_info
            state.patient_info["patient_id"] = patient_id
            state.patient_info["is_new_patient"] = is_new

            # build datetimes
            start_dt = datetime.combine(appointment_date, appointment_time)
            end_dt = start_dt + timedelta(minutes=duration_minutes)

            # book calendar
            event_id = self.calendar_api.book_slot(self.calendar_id, f"{patient_info.get('first_name')} {patient_info.get('last_name')}", start_dt, end_dt, summary_extra=doctor, location=patient_info.get("address"))
            if not event_id:
                state.errors.append("Failed to create calendar event")
                return state

            # create confirmation number
            state.confirmation_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            state.is_confirmed = True
            state.appointment = {
                "doctor": doctor,
                "date": appointment_date.isoformat(),
                "time": appointment_time.strftime("%H:%M"),
                "event_id": event_id,
                "duration_minutes": duration_minutes,
                "reason": reason
            }

            # notify via comm manager
            message = (
                f"Appointment Confirmed ✅\n"
                f"Name: {patient_info.get('first_name')} {patient_info.get('last_name')}\n"
                f"Doctor: {doctor}\n"
                f"Date: {appointment_date.isoformat()}\n"
                f"Time: {appointment_time.strftime('%H:%M')}\n"
                f"Confirmation#: {state.confirmation_number}"
            )

            # send to patient
            if patient_info.get("email"):
                try:
                    self.comm_manager.send_email(patient_info.get("email"), "Appointment Confirmation", message)
                except Exception:
                    pass
            if patient_info.get("phone"):
                try:
                    self.comm_manager.send_sms(patient_info.get("phone"), message)
                except Exception:
                    pass

            # TODO: doctor contact can be configured per doctor
            doctor_phone = patient_info.get("doctor_phone")  # optional
            doctor_email = patient_info.get("doctor_email")  # optional
            if doctor_email:
                try:
                    self.comm_manager.send_email(doctor_email, "New Appointment Scheduled", message)
                except Exception:
                    pass
            if doctor_phone:
                try:
                    self.comm_manager.send_sms(doctor_phone, message)
                except Exception:
                    pass

            return state

        except Exception as e:
            state.errors.append(str(e))
            return state
