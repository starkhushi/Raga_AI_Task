from utils.data_model import init_db, Patient, SessionLocal
from datetime import datetime

init_db()

session = SessionLocal()
sample_patient = Patient(
    patient_id="P001",
    first_name="John",
    last_name="Doe",
    date_of_birth=datetime.strptime("1980-01-01", "%Y-%m-%d"),
    phone="1234567890",
    email="john.doe@example.com"
)

session.add(sample_patient)
session.commit()
session.close()
print("Sample patient added.")
