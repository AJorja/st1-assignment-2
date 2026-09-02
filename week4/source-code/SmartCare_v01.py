# Task 1
# Create and run a simple Python file with basic input/output statements

print("Welcome to SmartCare: Community Clinic Appointment Booking System!")

# First Appointment
patient1_name = "Alice Smith"
practitioner1_name = "Dr. John Doe"
appointment1_time = "2024-07-20 10:00 AM"

print(
    f"Patient: {patient1_name} | "
    f"Practitioner: {practitioner1_name} | "
    f"Time: {appointment1_time}"
)

# Second Appointment
patient2_name = "Bob Johnson"
practitioner2_name = "Dr. Jane Roe"
appointment2_time = "2024-07-20 11:30 AM"

print(
    f"Patient: {patient2_name} | "
    f"Practitioner: {practitioner2_name} | "
    f"Time: {appointment2_time}"
)

# Task 1 Enhanced
# Use lists, dictionaries and functions to enhance the Python file

appointments = []


def book_appointment(patient_name, practitioner_name, appointment_time):
    if not patient_name:
        raise ValueError("Patient name cannot be empty")
    for existing in appointments:
        if (existing["practitioner"] == practitioner_name
                and existing["time"] == appointment_time):
            raise ValueError(
                f"{practitioner_name} is already booked at {appointment_time}"
            )

    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }

    appointments.append(appointment)


def display_appointments():
    if not appointments:
        print("No appointments recorded.")
        return

    for appointment in appointments:
        print(
            f"Patient: {appointment['patient']} | "
            f"Practitioner: {appointment['practitioner']} | "
            f"Time: {appointment['time']}"
        )


print("Welcome to SmartCare: The Clinical Appointment Booking System!")

book_appointment(
    "Alice Smith",
    "Dr. John Doe",
    "2024-07-20 10:00 AM"
)

book_appointment(
    "Bob Johnson",
    "Dr. Jane Roe",
    "2024-07-20 11:30 AM"
)

display_appointments()
