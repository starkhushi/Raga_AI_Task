from sqlalchemy import create_engine, Column, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)  # set echo=True for SQL logs
SessionLocal = sessionmaker(bind=engine)

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    insurance_carrier = Column(String, nullable=True)
    member_id = Column(String, nullable=True)
    group_number = Column(String, nullable=True)
    last_visit = Column(Date, nullable=True)
    is_new_patient = Column(Boolean, default=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def find_patient(session, first_name, last_name, dob):
    """
    dob is expected as 'YYYY-MM-DD' string or a date object.
    """
    if isinstance(dob, str):
        dob_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
    elif isinstance(dob, datetime.date):
        dob_date = dob
    else:
        return None

    return session.query(Patient).filter(
        Patient.first_name == first_name,
        Patient.last_name == last_name,
        Patient.date_of_birth == dob_date
    ).first()
