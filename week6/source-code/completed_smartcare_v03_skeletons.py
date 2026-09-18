"""SmartCare v0.3 domain class skeletons.

Structural skeletons only: the goal is consistency with the
UML model, not working behaviour. Method bodies are placeholders 

"""

# The permitted appointment statuses (FR-03, FR-06, FR-07). This is an assumption: v0.2 records the full status # set as an open question, because the client has never stated it.
BOOKED = "Booked"
ATTENDED = "Attended"
DID_NOT_ATTEND = "Did Not Attend"
CANCELLED = "Cancelled"

APPOINTMENT_STATUSES = (BOOKED, ATTENDED, DID_NOT_ATTEND, CANCELLED)


class Patient:
    """A person the clinic holds a record for (FR-01).

    Identified by name only. Fields beyond the name are provisional in v0.2,
    so none are modelled here.
    """

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        """Return the patient's name (FR-01)."""
        pass

    def matches_name(self, search_term):
        """Report whether the name matches the search term (FR-11 amended).

        Case-insensitive partial match.
        """
        pass

    def is_valid(self):
        """Report whether the name is present (FR-05)."""
        pass


class Practitioner:
    """A practitioner the clinic holds a record for (FR-02).

    Identified by name only. Specialty and other fields are an open question
    in v0.2 and are deliberately not modelled.
    """

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        """Return the practitioner's name (FR-02)."""
        pass

    def is_valid(self):
        """Report whether the name is present (FR-05)."""
        pass


class Appointment:
    """A booking of one patient with one practitioner at one date and time.

    Traces to FR-03, FR-06, FR-07, FR-08, FR-09, FR-10, FR-12.

    The patient, practitioner and date/time are set once at construction and
    have no setters, which is how NFR-06 is enforced structurally: a status
    change cannot alter them because there is no way to alter them.
    """

    def __init__(self, patient, practitioner, date_time):
        self.__patient = patient
        self.__practitioner = practitioner
        self.__date_time = date_time
        self.__status = BOOKED  # FR-03

    def get_patient(self):
        """Return the patient this appointment is for (FR-03)."""
        pass

    def get_practitioner(self):
        """Return the practitioner this appointment is with (FR-03)."""
        pass

    def get_date_time(self):
        """Return the date and time of this appointment (FR-03)."""
        pass

    def get_status(self):
        """Return the current status (FR-03, FR-06, FR-07)."""
        pass

    def cancel(self):
        """Set the status to Cancelled (FR-07).

        The appointment is retained rather than removed (FR-08).
        """
        pass

    def mark_attended(self):
        """Record that the patient attended (FR-06)."""
        pass

    def mark_did_not_attend(self):
        """Record that the patient did not attend (FR-06)."""
        pass

    def is_booked(self):
        """Report whether the status is Booked (FR-09, FR-10, FR-12)."""
        pass

    def is_cancelled(self):
        """Report whether the status is Cancelled (FR-10 amended)."""
        pass

    def is_for(self, practitioner):
        """Report whether this appointment is with the given practitioner (FR-04, FR-10)."""
        pass

    def occurs_at(self, date_time):
        """Report whether this appointment is at the given date and time (FR-04)."""
        pass

    def occurs_between(self, start, end):
        """Report whether this appointment falls in the date range (FR-12)."""
        pass


class AppointmentBook:
    """The clinic's collection of appointments (FR-03, FR-04, FR-05, FR-08 to FR-12).

    This class exists because five requirements ask questions no single
    Appointment can answer: whether a practitioner is already booked (FR-04),
    which appointments are currently Booked (FR-09), which belong to a
    practitioner and how many of theirs were cancelled (FR-10), and how many
    fall in a date range (FR-12). It holds the records and answers those
    questions; it does not display or store anything.
    """

    def __init__(self):
        self.__appointments = []

    def book(self, patient, practitioner, date_time):
        """Create and store an appointment with a status of Booked (FR-03).

        Rejects the booking where the practitioner is already booked at that
        date and time (FR-04), or where either name is empty (FR-05),
        reporting which rule was broken. The rejection is returned to the
        caller rather than displayed (NFR-02).
        """
        pass

    def is_practitioner_free(self, practitioner, date_time):
        """Report whether the practitioner is free at that date and time (FR-04)."""
        pass

    def booked_appointments(self):
        """Return every appointment with a status of Booked (FR-09)."""
        pass

    def appointments_for(self, practitioner):
        """Return the Booked appointments for a practitioner (FR-10 amended)."""
        pass

    def cancelled_count_for(self, practitioner):
        """Return the count of cancelled appointments for a practitioner (FR-10 amended)."""
        pass

    def count_between(self, start, end):
        """Count appointments with a status of Booked or Attended in a range (FR-12 amended)."""
        pass


class PatientRegister:
    """The clinic's collection of patient records (FR-01, FR-11).

    Patients need a home for FR-01 to be satisfied as stored, retrievable
    state, and FR-11 needs something to search across.

    There is deliberately no PractitionerRegister. FR-02 requires practitioner
    records to be stored, so that need is real, but no requirement searches,
    lists or counts practitioners, which would leave the class with one
    operation and no query to justify it. The FR-02 storage need is therefore
    unmet in v0.3 and recorded as an open question rather than closed by
    adding a class the requirements do not ask for.
    """

    def __init__(self):
        self.__patients = []

    def add_patient(self, name):
        """Create and store a patient record (FR-01)."""
        pass

    def find_by_name(self, search_term):
        """Return every patient matching the term (FR-11 amended)."""
        pass
