import streamlit as st
from datetime import datetime, date, time, timedelta
from utils.calendar_api import GoogleCalendarAPI
from utils.communication import CommunicationManager
from utils.data_model import SessionLocal, Patient, init_db, find_patient
from config import GOOGLE_CREDENTIALS_JSON
import os

# Initialize DB & services
init_db()
db = SessionLocal()
calendar_api = GoogleCalendarAPI(GOOGLE_CREDENTIALS_JSON)
comm = CommunicationManager()
calendar_id = "khushi886987@gmail.com"

st.set_page_config(page_title="Medical Appointment Scheduler", layout="centered")

# Greeting message at the start
st.title("📅 Medical Appointment Scheduler")
st.markdown("👋 **Welcome!** Please fill in your details below to schedule an appointment.")

with st.form("appointment_form"):
    st.subheader("Patient Information")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    dob = st.date_input("Date of Birth", value=date(2000, 1, 1))
    email = st.text_input("Email")
    phone = st.text_input("Phone Number (E.164, e.g. +9190XXXXXXXX)")
    address = st.text_area("Address")

    st.subheader("Appointment Details")
    appointment_date = st.date_input("Appointment Date", value=(date.today() + timedelta(days=1)))
    appointment_time = st.time_input("Appointment Time", value=time(hour=10, minute=0))
    doctor = st.selectbox("Doctor", ["Dr. Smith", "Dr. Gupta", "Dr. Patel"])
    reason = st.text_area("Reason for Appointment")
    insurance = st.text_input("Insurance Provider (Optional)")

    submit = st.form_submit_button("📌 Book an Appointment")

if submit:
    # basic validation
    if not (first_name and last_name and phone):
        st.error("Please fill required fields: First Name, Last Name, Phone.")
    else:
        # Check existing patient
        existing = find_patient(db, first_name, last_name, dob.isoformat())
        if existing:
            patient_id = existing.patient_id
            existing.phone = phone
            existing.email = email
            existing.address = address
            existing.insurance_carrier = insurance
            existing.last_visit = datetime.now().date()
            db.add(existing)
            db.commit()
        else:
            patient_id = f"P{int(datetime.now().timestamp())}"
            new_patient = Patient(
                patient_id=patient_id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                phone=phone,
                email=email,
                address=address,
                insurance_carrier=insurance,
                last_visit=datetime.now().date(),
                is_new_patient=True
            )
            db.add(new_patient)
            db.commit()

        # Book in Google Calendar
        start_dt = datetime.combine(appointment_date, appointment_time)
        end_dt = start_dt + timedelta(minutes=30)

        event_id = calendar_api.book_slot(
            calendar_id,
            f"{first_name} {last_name}",
            start_dt,
            end_dt,
            summary_extra=doctor,
            location=address
        )

        if not event_id:
            st.error("Failed to create calendar event.")
        else:
            confirmation_number = f"CNF{int(datetime.now().timestamp())}"
            message = (
                f"✅ Appointment Confirmed\n"
                f"Name: {first_name} {last_name}\n"
                f"Doctor: {doctor}\n"
                f"Date: {appointment_date.isoformat()}\n"
                f"Time: {appointment_time.strftime('%H:%M')}\n"
                f"Confirmation#: {confirmation_number}\n\n"
                "🙏 Thanks for your appointment! See you there."
            )

            errors = []
            # Send to patient
            if email:
                try:
                    comm.send_email(email, "Appointment Confirmation", message)
                except Exception as e:
                    errors.append(f"Email error: {e}")

            if phone:
                try:
                    comm.send_sms(phone, message)
                except Exception as e:
                    errors.append(f"SMS error: {e}")

            # Send to doctor
            doctor_email_map = {
                "Dr. Smith": "dr.smith@example.com",
                "Dr. Gupta": "dr.gupta@example.com",
                "Dr. Patel": "dr.patel@example.com"
            }
            doctor_phone_map = {
                "Dr. Smith": None,
                "Dr. Gupta": None,
                "Dr. Patel": None
            }

            doc_email = doctor_email_map.get(doctor)
            doc_phone = doctor_phone_map.get(doctor)

            if doc_email:
                try:
                    comm.send_email(doc_email, "New Appointment Scheduled", message)
                except Exception as e:
                    errors.append(f"Doctor email error: {e}")

            if doc_phone:
                try:
                    comm.send_sms(doc_phone, message)
                except Exception as e:
                    errors.append(f"Doctor SMS error: {e}")

            # Success message with thank you note
            st.success("🎉 Appointment booked successfully!")
            st.markdown(f"**Confirmation Number:** `{confirmation_number}`")
            st.markdown(f"**Google Event ID:** `{event_id}`")
            st.markdown("🙏 **Thanks for your appointment! See you there.**")
            
            if errors:
                st.warning("Some notifications failed. See details below.")
                for err in errors:
                    st.write(f"- {err}")
