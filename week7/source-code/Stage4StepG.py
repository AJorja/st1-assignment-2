"""SmartCare v0.4 - Stage 4 step G refactored domain classes.

Patient and Practitioner are unchanged from steps B and C. Appointment is the
step D generated code with the four refactors recorded in the step G note:
mark_completed() added, Any replaced with the real domain types, constructor
validation added, and the domain exception renamed.
"""

from datetime import datetime
from enum import Enum


# ---------------------------------------------------------------- step B


class Patient:
    """A person the clinic holds a record for (FR-01).

    Identified by patient_id and name. Contact details are named in the
    Week 7 Assignment 2 discussion but no specific fields are given, and
    v0.2 records patient fields beyond the name as provisional, so none
    are modelled.
    """

    def __init__(self, patient_id: str, name: str):
        if not patient_id.strip():
            raise ValueError("Patient ID cannot be empty")
        if not name.strip():
            raise ValueError("Patient name cannot be empty")

        self.__patient_id: str = patient_id.strip()
        self.__name: str = name.strip()

    def get_patient_id(self) -> str:
        """Return the patient's identifier (FR-01)."""
        return self.__patient_id

    def get_name(self) -> str:
        """Return the patient's name (FR-01)."""
        return self.__name

    def matches_name(self, search_term: str) -> bool:
        """Report whether the name matches the search term (FR-11 amended).

        Case-insensitive partial match.
        """
        return search_term.strip().lower() in self.__name.lower()


# ---------------------------------------------------------------- step C


class Practitioner:
    """A practitioner the clinic holds a record for (FR-02).

    Identified by practitioner_id and name. Specialty is adopted from the
    Week 7 Assignment 2 discussion; v0.2 records practitioner fields beyond
    the name as an open question, so it is optional rather than required.
    """

    def __init__(self, practitioner_id: str, name: str, specialty: str = ""):
        if not practitioner_id.strip():
            raise ValueError("Practitioner ID cannot be empty")
        if not name.strip():
            raise ValueError("Practitioner name cannot be empty")

        self.__practitioner_id: str = practitioner_id.strip()
        self.__name: str = name.strip()
        self.__specialty: str = specialty.strip()

    def get_practitioner_id(self) -> str:
        """Return the practitioner's identifier (FR-02)."""
        return self.__practitioner_id

    def get_name(self) -> str:
        """Return the practitioner's name (FR-02)."""
        return self.__name

    def get_specialty(self) -> str:
        """Return the practitioner's specialty, which may be empty."""
        return self.__specialty


# ------------------------------------------------- step D, refactored at G


class AppointmentStatus(Enum):
    """Enumeration of valid appointment statuses."""
    SCHEDULED = "Scheduled"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class InvalidStatusTransitionError(Exception):
    """Raised when an appointment is asked to make an illegal status change."""
    pass


class Appointment:
    """Represents a scheduled appointment between a patient and a practitioner."""

    def __init__(self, appointment_id: str, patient: Patient,
                 practitioner: Practitioner, date_time: datetime) -> None:
        if not appointment_id.strip():
            raise ValueError("Appointment ID cannot be empty")
        if patient is None:
            raise ValueError("Appointment must have a patient")
        if practitioner is None:
            raise ValueError("Appointment must have a practitioner")
        if date_time is None:
            raise ValueError("Appointment must have a date and time")

        self.__appointment_id: str = appointment_id.strip()
        self.__patient: Patient = patient
        self.__practitioner: Practitioner = practitioner
        self.__date_time: datetime = date_time
        self.__status: AppointmentStatus = AppointmentStatus.SCHEDULED

    # --- Getters ---
    def get_appointment_id(self) -> str:
        return self.__appointment_id

    def get_patient(self) -> Patient:
        return self.__patient

    def get_practitioner(self) -> Practitioner:
        return self.__practitioner

    def get_date_time(self) -> datetime:
        return self.__date_time

    def get_status(self) -> AppointmentStatus:
        return self.__status

    # --- Business operations ---
    def cancel(self) -> None:
        """Cancels the appointment unless already cancelled or completed."""
        if self.__status in (AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED):
            raise InvalidStatusTransitionError(
                f"Cannot cancel an appointment that is already {self.__status.value}."
            )
        self.__status = AppointmentStatus.CANCELLED

    def mark_completed(self) -> None:
        """Records that the appointment took place."""
        if self.__status is not AppointmentStatus.SCHEDULED:
            raise InvalidStatusTransitionError(
                f"Cannot complete an appointment that is {self.__status.value}."
            )
        self.__status = AppointmentStatus.COMPLETED

    # --- Status checks ---
    def is_scheduled(self) -> bool:
        return self.__status == AppointmentStatus.SCHEDULED

    def is_cancelled(self) -> bool:
        return self.__status == AppointmentStatus.CANCELLED

    # --- Relationship and time checks ---
    def is_for(self, practitioner: Practitioner) -> bool:
        return self.__practitioner == practitioner

    def occurs_at(self, date_time: datetime) -> bool:
        return self.__date_time == date_time

    def occurs_between(self, start: datetime, end: datetime) -> bool:
        return start <= self.__date_time <= end


# ------------------------------------------------- re-run the step F checks


print("1. Create valid objects")
patient = Patient("P001", "Alice Smith")
practitioner = Practitioner("D001", "John Doe", "GP")
appointment = Appointment("A001", patient, practitioner,
                          datetime(2026, 9, 25, 10, 0))
print("   status:", appointment.get_status())
print("   is_scheduled:", appointment.is_scheduled())

print()
print("2. Invalid input")
try:
    bad_patient = Patient("", "")
    print("   FAIL - Patient created with empty id and name")
except Exception as error:
    print("   Patient raised:", type(error).__name__, "-", error)

try:
    bad_appointment = Appointment("", None, None, None)
    print("   FAIL - Appointment created with empty id and no patient")
except Exception as error:
    print("   Appointment raised:", type(error).__name__, "-", error)

print()
print("3. Cancel a scheduled appointment")
appointment.cancel()
print("   status:", appointment.get_status())
print("   object retained:", appointment.get_appointment_id())

print()
print("4. Cancel again (illegal repeated transition)")
try:
    appointment.cancel()
    print("   FAIL - second cancel succeeded")
except Exception as error:
    print("   raised:", type(error).__name__, "-", error)

print()
print("5. COMPLETED reachability")
second = Appointment("A002", patient, practitioner,
                     datetime(2026, 9, 26, 11, 0))
second.mark_completed()
print("   status after mark_completed:", second.get_status())

print()
print("6. Complete an already cancelled appointment")
try:
    appointment.mark_completed()
    print("   FAIL - completed a cancelled appointment")
except Exception as error:
    print("   raised:", type(error).__name__, "-", error)
