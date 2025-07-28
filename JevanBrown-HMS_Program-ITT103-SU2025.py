import random
from datetime import datetime

class Person:
    def __init__(self, name, age, gender):
        # Initialize attributes of a person
        self.name = name       
        self.age = age          
        self.gender = gender    
    
    def display_info(self):
        # Display basic information about the person
        return f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}"

class Patient(Person):
    def __init__(self, name, age, gender):
        # Initialize with parent class attributes
        super().__init__(name, age, gender)
        # Patient-specific attributes
        self.patient_id = self.generate_id()  
        self.appointments = []                
        self.has_insurance = False
    
    def generate_id(self):
        return f"PAT-{random.randint(1000, 9999)}"
    
    def book_appointment(self, appointment):
        self.appointments.append(appointment)
    
    def view_profile(self):
        # Get basic info from parent class
        info = super().display_info()
        # Format appointment details if any exist
        appointments_info = "\n".join([
            f"Appointment ID: {appt.appointment_id}, "
            f"Doctor: {appt.doctor.name}, "
            f"Date: {appt.date}, "
            f"Time: {appt.time}"
            for appt in self.appointments
        ])
        return (f"{info}\nPatient ID: {self.patient_id}\n"
                f"Insurance: {'Yes' if self.has_insurance else 'No'}\n"
                f"Appointments:\n{appointments_info if self.appointments else 'No appointments'}")

class Doctor(Person):
    def __init__(self, name, age, gender, specialty):
        # Initialize with parent class attributes
        super().__init__(name, age, gender)
        # Doctor-specific attributes
        self.doctor_id = self.generate_id()  
        self.specialty = specialty          
        self.schedule = []                 
    
    def generate_id(self):
        return f"DOC-{random.randint(1000, 9999)}"
    
    def add_available_time(self, date, time):
        self.schedule.append((date, time))
    
    def is_available(self, date, time):
        # Check if doctor is available at a specific date and time
        return (date, time) in self.schedule
    
    def view_schedule(self):
        # Display complete doctor information including schedule
        schedule_info = "\n".join([
            f"Date: {date}, Time: {time}" 
            for date, time in self.schedule
        ])
        return (f"{super().display_info()}\n"
                f"Doctor ID: {self.doctor_id}\n"
                f"Specialty: {self.specialty}\n"
                f"Available Schedule:\n"
                f"{schedule_info if self.schedule else 'No available schedule'}")

class Appointment:
    def __init__(self, patient, doctor, date, time):
        # Initialize appointment attributes
        self.appointment_id = f"APT-{random.randint(1000, 9999)}"  
        self.patient = patient      
        self.doctor = doctor        
        self.date = date            
        self.time = time            
        self.status = "Scheduled"   
        self.services = []          
    
    def confirm(self):
        # Change appointment status to Confirmed
        self.status = "Confirmed"
    
    def cancel(self):
        # Change appointment status to Cancelled
        self.status = "Cancelled"
    
    def add_service(self, service_name, fee):
        # Add an additional service to the appointment
        self.services.append({
            "name": service_name,
            "fee": fee             
        })
    
    def generate_bill(self):
        # Generate a formatted bill/receipt for the appointment

        # Base consultation fee
        consultation_fee = 3000  # JMD
        # Calculate total including additional services
        total = consultation_fee + sum(service["fee"] for service in self.services)
        
        # Apply insurance discount if patient has insurance
        if self.patient.has_insurance:
            total *= 0.85  # 15% discount
            insurance_note = "\n(15% insurance discount applied)"
        else:
            insurance_note = ""
        
        # Add 15% tax
        taxed_total = total * 1.15
        
        # Build the receipt 
        bill = "\n============ BILL ===========\n"
        bill += "\n=== OMEGA MEDICAL CENTRE ==="
        bill += f"\nAppointment ID: {self.appointment_id}"
        bill += f"\nPatient: {self.patient.name} ({self.patient.patient_id})"
        bill += f"\nDoctor: {self.doctor.name} ({self.doctor.doctor_id})"
        bill += f"\nDate: {self.date}, Time: {self.time}"
        bill += "\n\nServices:"
        bill += f"\n- Consultation: JMD ${consultation_fee}"
        
        # Add each additional service to the bill
        for service in self.services:
            bill += f"\n- {service['name']}: JMD ${service['fee']}"
        
        # Add total and closing
        bill += f"\n\nSUBTOTAL: JMD ${total:.2f}{insurance_note}"
        bill += f"\nTOTAL after 15% tax: JMD ${taxed_total:.2f}"
        bill += "\n\nThank you for choosing our Omega Medical!"
        bill += "\n Follow us on all socials @OmegaMEdical"
        return bill

class HospitalSystem:
    def __init__(self):
        # Initialize data storage
        self.patients = {}      
        self.doctors = {}       
        self.appointments = [] 
    
    def add_patient(self, name, age, gender):
        # Register a new patient in the system
        # Create new Patient object
        patient = Patient(name, age, gender)
        # Add to patients dictionary
        self.patients[patient.patient_id] = patient
        return patient
    
    def add_doctor(self, name, age, gender, specialty):
        # Register a new doctor in the system
        # Create new Doctor object
        doctor = Doctor(name, age, gender, specialty)
        # Add to doctors dictionary
        self.doctors[doctor.doctor_id] = doctor
        return doctor
    
    def book_appointment(self, patient_id, doctor_id, date, time):
        # Book a new appointment after validating availability
        # Validate patient exists
        patient = self.patients.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        
        # Validate doctor exists
        doctor = self.doctors.get(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        
        # Check doctor availability
        if not doctor.is_available(date, time):
            raise ValueError("Doctor not available at that time")
        
        # Check for existing appointments at same time
        for appointment in self.appointments:
            if (appointment.doctor.doctor_id == doctor_id and 
                appointment.date == date and 
                appointment.time == time and 
                appointment.status != "Cancelled"):
                raise ValueError("Doctor already has an appointment at that time")
        
        # Create and store new appointment
        appointment = Appointment(patient, doctor, date, time)
        self.appointments.append(appointment)
        # Add to patient's record
        patient.book_appointment(appointment)
        # Confirm appointment
        appointment.confirm()
        return appointment
    
    def cancel_appointment(self, appointment_id):
        # Cancel an existing appointment
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                appointment.cancel()
                return True
        return False
    
    def update_appointment(self, appointment_id, new_date, new_time):
        # Update an existing appointment
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                if appointment.doctor.is_available(new_date, new_time):
                    appointment.date = new_date
                    appointment.time = new_time
                    return True
                else:
                    raise ValueError("Doctor not available at the new time")
        return False
    
    def generate_bill(self, appointment_id):
        # Generate bill for a specific appointment
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                return appointment.generate_bill()
        raise ValueError("Appointment not found")
    
    def set_patient_insurance(self, patient_id, has_insurance):
        # Set insurance status for a patient
        patient = self.patients.get(patient_id)
        if patient:
            patient.has_insurance = has_insurance
            return True
        return False
    
    def validate_date(self, date_str):
        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def validate_time(self, time_str):
        # Validate time format (HH:MM AM/PM)
        try:
            datetime.strptime(time_str, "%I:%M %p")
            return True
        except ValueError:
            return False
    
    def calculate_age(self, birth_date_str):
        # Calculate age from birth date
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD")
    
    def validate_gender(self, gender):
        # Validate gender input
        valid_genders = ["M", "F", "Male", "Female"]
        if gender.capitalize() not in valid_genders:
            raise ValueError("Invalid gender. Please enter M or F")
        return gender
    
    def get_doctor_specialty(self):
        # Display specialty menu and get selection
        print("\nSelect Doctor Specialty:")
        print("1. General Practitioner")
        print("2. Dentist")
        print("3. Dermatologist")
        choice = input("Enter choice (1-3): ")
        
        specialties = {
            "1": "General Practitioner",
            "2": "Dentist",
            "3": "Dermatologist"
        }
        return specialties.get(choice, "General Practitioner")
    
    def get_services_for_specialty(self, specialty):
        # Return available services based on doctor's specialty
        services = {
            "General Practitioner": [
                {"name": "Basic Checkup", "fee": 1500},
                {"name": "Blood Test", "fee": 2000},
                {"name": "Medical", "fee": 2500}
            ],
            "Dentist": [
                {"name": "Dental Cleaning", "fee": 3000},
                {"name": "Tooth Extraction", "fee": 5000},
                {"name": "Dental Filling", "fee": 4000}
            ],
            "Dermatologist": [
                {"name": "Skin Examination", "fee": 3500},
                {"name": "Acne Treatment", "fee": 4500},
                {"name": "Biopsy", "fee": 6000}
            ]
        }
        return services.get(specialty, [])

def main():
    # Initialize hospital system
    hospital = HospitalSystem()
    
    # Main program loop
    while True:
        # Display menu
        print("\n=== OMEGA MEDICAL MANAGEMENT SYSTEM ===")
        print("\n================= Menu ================")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. Cancel/Update Appointment")
        print("5. Generate Bill")
        print("6. View Patient Profile")
        print("7. View Doctor Schedule")
        print("8. Set Patient Insurance")
        print("9. Exit")
        
        # Get user choice
        choice = input("Enter your choice: ")
        
        try:
            # Process user choice
            if choice == '1':
                # Add new patient
                name = input("Enter patient name: ")
                birth_date = input("Enter patient birth date (YYYY-MM-DD): ")
                age = hospital.calculate_age(birth_date)
                gender = hospital.validate_gender(input("Enter patient gender (M/F): "))
                patient = hospital.add_patient(name, age, gender)
                
                # Set insurance status
                insurance = input("Does the patient have insurance? (yes/no): ").lower()
                if insurance == 'yes':
                    hospital.set_patient_insurance(patient.patient_id, True)
                
                print(f"Patient added successfully. Patient ID: {patient.patient_id}")
            
            elif choice == '2':
                # Add new doctor
                name = input("Enter doctor name: ")
                birth_date = input("Enter doctor birth date (YYYY-MM-DD): ")
                age = hospital.calculate_age(birth_date)
                gender = hospital.validate_gender(input("Enter doctor gender (M/F): "))
                specialty = hospital.get_doctor_specialty()
                doctor = hospital.add_doctor(name, age, gender, specialty)
                print(f"Doctor added successfully. Doctor ID: {doctor.doctor_id}")
                
                # Add available time slots
                while True:
                    date = input("Enter available date (YYYY-MM-DD) or 'done' to finish: ")
                    if date.lower() == 'done':
                        break
                    if not hospital.validate_date(date):
                        print("Invalid date format. Please use YYYY-MM-DD")
                        continue
                    time = input("Enter available time (e.g., 10:00 AM): ")
                    if not hospital.validate_time(time):
                        print("Invalid time format. Please use HH:MM AM/PM")
                        continue
                    doctor.add_available_time(date, time)
                    print("Time slot added successfully.")
            
            elif choice == '3':
                # Book new appointment
                patient_id = input("Enter patient ID: ")
                doctor_id = input("Enter doctor ID: ")
                date = input("Enter appointment date (YYYY-MM-DD): ")
                if not hospital.validate_date(date):
                    raise ValueError("Invalid date format. Please use YYYY-MM-DD")
                time = input("Enter appointment time (e.g., 10:00 AM): ")
                if not hospital.validate_time(time):
                    raise ValueError("Invalid time format. Please use HH:MM AM/PM")
                
                appointment = hospital.book_appointment(patient_id, doctor_id, date, time)
                print(f"Appointment booked successfully. Appointment ID: {appointment.appointment_id}")
                
                # Add services from predefined list
                doctor = hospital.doctors.get(doctor_id)
                if doctor:
                    services = hospital.get_services_for_specialty(doctor.specialty)
                    print("\nAvailable Services:")
                    for i, service in enumerate(services, 1):
                        print(f"{i}. {service['name']} - JMD ${service['fee']}")
                    
                    while True:
                        service_choice = input("Select service (1-3) or 'done' to finish: ")
                        if service_choice.lower() == 'done':
                            break
                        try:
                            selected = services[int(service_choice)-1]
                            appointment.add_service(selected['name'], selected['fee'])
                            print(f"Added {selected['name']} to appointment")
                        except (ValueError, IndexError):
                            print("Invalid selection. Please try again.")
            
            elif choice == '4':
                # Cancel or update appointment
                appointment_id = input("Enter appointment ID: ")
                action = input("Do you want to 'cancel' or 'update' this appointment? ").lower()
                
                if action == 'cancel':
                    if hospital.cancel_appointment(appointment_id):
                        print("Appointment cancelled successfully.")
                    else:
                        print("Appointment not found.")
                elif action == 'update':
                    new_date = input("Enter new appointment date (YYYY-MM-DD): ")
                    if not hospital.validate_date(new_date):
                        print("Invalid date format. Please use YYYY-MM-DD")
                        continue
                    new_time = input("Enter new appointment time (e.g., 10:00 AM): ")
                    if not hospital.validate_time(new_time):
                        print("Invalid time format. Please use HH:MM AM/PM")
                        continue
                    
                    if hospital.update_appointment(appointment_id, new_date, new_time):
                        print("Appointment updated successfully.")
                    else:
                        print("Failed to update appointment. Doctor may not be available.")
                else:
                    print("Invalid action. Please enter 'cancel' or 'update'")
            
            elif choice == '5':
                # Generate bill for appointment
                appointment_id = input("Enter appointment ID to generate bill: ")
                bill = hospital.generate_bill(appointment_id)
                print(bill)
            
            elif choice == '6':
                # View patient profile
                patient_id = input("Enter patient ID: ")
                patient = hospital.patients.get(patient_id)
                if patient:
                    print(patient.view_profile())
                else:
                    print("Patient not found.")
            
            elif choice == '7':
                # View doctor schedule
                doctor_id = input("Enter doctor ID: ")
                doctor = hospital.doctors.get(doctor_id)
                if doctor:
                    print(doctor.view_schedule())
                else:
                    print("Doctor not found.")
            
            elif choice == '8':
                # Set patient insurance status
                patient_id = input("Enter patient ID: ")
                insurance = input("Does the patient have insurance? (yes/no): ").lower()
                if insurance in ['yes', 'no']:
                    hospital.set_patient_insurance(patient_id, insurance == 'yes')
                    print("Insurance status updated successfully.")
                else:
                    print("Invalid input. Please enter 'yes' or 'no'")
            
            elif choice == '9':
                # Exit program
                print("Exiting the system. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
