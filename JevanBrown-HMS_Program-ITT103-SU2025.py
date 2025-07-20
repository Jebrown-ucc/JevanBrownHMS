import random

class Person:
    def __init__(self, name, age, gender):
        # Initialize attributes odf a person
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
        
        # Build the receipt 
        bill = "\n=== HOSPITAL BILL ===\n"
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
        bill += f"\n\nTOTAL: JMD ${total}"
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
    
    def generate_bill(self, appointment_id):
        # Generate bill for a specific appointment
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                return appointment.generate_bill()
        raise ValueError("Appointment not found")

def main():
    # Initialize hospital system
    hospital = HospitalSystem()
    
    # Main program loop
    while True:
        # Display menu
        print("\n=== HOSPITAL MANAGEMENT SYSTEM ===")
        print("\n=== Menu ===")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. Cancel Appointment")
        print("5. Generate Bill")
        print("6. View Patient Profile")
        print("7. View Doctor Schedule")
        print("8. Exit")
        
        # Get user choice
        choice = input("Enter your choice: ")
        
        try:
            # Process user choice
            if choice == '1':
                # Add new patient
                name = input("Enter patient name: ")
                age = int(input("Enter patient age: "))
                gender = input("Enter patient gender (M or F): ")
                patient = hospital.add_patient(name, age, gender)
                print(f"Patient added successfully. Patient ID: {patient.patient_id}")
            
            elif choice == '2':
                # Add new doctor
                name = input("Enter doctor name: ")
                age = int(input("Enter doctor age: "))
                gender = input("Enter doctor gender (M or F): ")
                specialty = input("Enter doctor specialty: ")
                doctor = hospital.add_doctor(name, age, gender, specialty)
                print(f"Doctor added successfully. Doctor ID: {doctor.doctor_id}")
                
                # Add available time slots
                while True:
                    date = input("Enter available date (YYYY-MM-DD) or 'done' to finish: ")
                    if date.lower() == 'done':
                        break
                    time = input("Enter available time (e.g., 10:00 AM): ")
                    doctor.add_available_time(date, time)
                    print("Time slot added successfully.")
            
            elif choice == '3':
                # Book new appointment
                patient_id = input("Enter patient ID: ")
                doctor_id = input("Enter doctor ID: ")
                date = input("Enter appointment date (YYYY-MM-DD): ")
                time = input("Enter appointment time (e.g., 10:00 AM): ")
                
                appointment = hospital.book_appointment(patient_id, doctor_id, date, time)
                print(f"Appointment booked successfully. Appointment ID: {appointment.appointment_id}")
                
                # Add additional services
                while True:
                    service = input("Enter service name (or 'done' to finish): ")
                    if service.lower() == 'done':
                        break
                    fee = float(input("Enter service fee: "))
                    appointment.add_service(service, fee)
                    print("Service added successfully.")
            
            elif choice == '4':
                # Cancel existing appointment
                appointment_id = input("Enter appointment ID to cancel: ")
                if hospital.cancel_appointment(appointment_id):
                    print("Appointment cancelled successfully.")
                else:
                    print("Appointment not found.")
            
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