# 📅 Medical Appointment Scheduler

A **Streamlit-based Medical Appointment Scheduler** designed to streamline booking appointments, managing patient data, sending notifications, and integrating with Google Calendar. This project aims to simplify appointment management for clinics while improving communication with patients and doctors.

---
## 🖼️ Screenshots

**1. Appointment Form**  
![Appointment Form](screenshots/form.png)

**2. Appointment Confirmation**  
![Confirmation](screenshots/confirmation.png)

---

## 🎬 Demo Video

Watch the demo of the application in action:

[📽️ View Demo on Google Drive]([https://drive.google.com/file/d/your-demo-video-id/view?usp=sharing](https://drive.google.com/file/d/1rkHlmzFSIs5SZPE__7zMy2FLbgWY7XBp/view?usp=sharing))

---
## 🎯 Features

1. **Patient Information Management**
   - Add new patients and store details including name, DOB, phone, email, address, and insurance.
   - Update existing patient records automatically when booking new appointments.

2. **Appointment Scheduling**
   - Choose appointment date, time, doctor, and reason for visit.
   - Automatically book appointments in **Google Calendar**.

3. **Notifications**
   - Send **email** and **SMS** notifications to patients and doctors with appointment details.
   - Includes confirmation numbers for easy reference.

4. **Database Integration**
   - Stores patient and appointment data in **SQLite** for record-keeping and analytics.

5. **User-Friendly Interface**
   - Streamlit web interface with forms for easy appointment booking.
   - Friendly greetings and thank-you messages for patients.

6. **Customizable**
   - Easily change doctors, email/SMS templates, or calendar settings.

---

## 🛠️ Approach / Implementation

- **Frontend:** Streamlit for creating an interactive, user-friendly interface.
- **Backend:**
  - **Google Calendar API** to automatically schedule appointments and track events.
  - **Twilio API** for sending SMS notifications.
  - **SMTP (Email)** for sending appointment confirmations.
- **Database:** SQLAlchemy with SQLite for storing patient and appointment data.
- **Workflow:**
  1. Patient fills the form in the web app.
  2. Checks if patient exists in the database or creates a new record.
  3. Books an appointment in Google Calendar.
  4. Sends notifications to patient and doctor.
  5. Displays confirmation number and Google Calendar event ID.

---

## Developed with ❤️ by Khushi
