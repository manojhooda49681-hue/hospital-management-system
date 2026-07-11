import streamlit as st
import sqlite3


# 1. database connect 
conn = sqlite3.connect("hospital.db")
c = conn.cursor()


# 2. table banao
c.execute('''CREATE TABLE IF NOT EXISTS patients
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT, age INTEGER, gender TEXT, disease TEXT, room_no INTEGER )''')


c.execute('''CREATE TABLE IF NOT EXISTS doctors
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT, specialization TEXT, contact TEXT)''')


c.execute('''CREATE TABLE IF NOT EXISTS appointments
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          patient_id INTEGER, doctor_id INTEGER,
          date TEXT, time TEXT)''')
conn.commit()



st.title("Hospital Management System")

menu = ["Add Patients", "View Patients", "Add Doctors", "View Doctors", "Book Appointment", "View Appointment"]
choice = st.sidebar.selectbox("Menu", menu)

 
# --- PATIENT ---
if choice == "Add Patients":
    st.subheader("Add New Patient")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender",["Male", "Female", "Other"])
    disease = st.text_input("Disease")
    room_no = st.number_input("Room NO", 1)
    if st.button("Add Patient"):
        c.execute("INSERT INTO patients(name, age, gender, disease, room_no) VALUES (?,?,?,?,?)",
                  (name,age,gender,disease,room_no))
        conn.commit()
        st.success("Patient Added")


elif choice == "View Patients":
    st.subheader("All Patients")
    c.execute("SELECT * FROM patients")
    for row in c.fetchall():
        st.write(f"**ID:** {row[0]} | **Name:** {row[1]} | **Age:** {row[2]} | **Gender:** {row[3]} | **Disease:** {row[4]}")

 
# --- Doctor ---
elif choice == "Add Doctor":
    st.subheader("Add New Doctor")
    name = st.text_input("Doctor Name")
    specialization = st.text_input("Specialization")
    contact = st.text_input("Contact No.")
    if st.button("Add doctor"):
        c.execute("INSERT INTO doctors(name,specilization,contact) VALUE (?,?,?,?,?,?,?)",
                  (name,specialization,contact))
        conn.commit()
        st.success("Doctor Added")

elif choice == "View Doctors":
    st.subheader("All Doctors")
    c.execute("SELECT * FROM doctors")
    for row in c.fetchall():
        st.write(f"**ID:** {row[0]} | **Dr. {row[1]}** | **Spec:** {row[2]} | **Contact** {row[3]}")


# --- APPOINTMENT ---
elif choice == "Book Appointment":
    st.subhheader("Book Appointment")

# Dropdown se patient aur doctor select
c.execute("SELECT id,name FROM patients")
patients = c.fetchall()
patient_dict = {p[1]: p[0] for p in patients}



c.execute("SELECT id,name FROM doctors")
doctors = c.fetchall()
doctor_dict = {d[1]: d[0] for d in doctors}

patient_name = st.selectbox("Select Patient", list(patient_dict.keys()))
doctor_name = st.selectbox("Select Doctor", list(doctor_dict.keys()))
date = st.date_input("Date")
time = st.time_input("Time")


menu = ["Add Patient", "Add Doctor", "Book Appointment", "View Data"]
choice = st.sidebar.selectbox("Menu", menu)

name = st.text_input("Doctor Name")
specialization = st.text_input("Specialization")
contact = st.text_input("Contact No.")
    
            
if st.button("Add Doctor"):
        if name and specialization:
            c.execute("INSERT INTO doctors(name, specialization, contact) VALUES (?,?,?)", 
                      (name, specialization, contact))
            conn.commit()
            st.success(f"Doctor {name} added successfully!")
        else:
            st.error("Please fill Name and Specialization")
# if st.button("Book"):
#     c.execute("INSERT INTO appointments(patient_id, doctor_id, date, time) VALUE (?,?,?,?,?,?,?),"
#               (patient_dict[patient_name], doctor_dict[doctor_name], str(date), str(time)))
#     conn.commit()
#     st.success("Appointment Booked") 

# elif choice == "View Appointments":
#     st.subheader("All Appointments")
#     c.execute('''SELECT a.id, p.name, d.name, a.date, a.time
#               FROM appointments a
#               JOIN patients p ON a.patient_id = p.id
#               JOIN doctors d ON a.doctor_id = d.id''')
    
#     for row in c.fetchall():     
#         st.write(f"**ID:** {row[0]} | **Patient:** {row[1]} | **Doctor:** Dr.{row[2]} | **Date:** {row[3]} | **Time:** {row[4]}")


# conn.close()


if st.button("Book"):
    if not patient_name or not doctor_name:
        st.error("Please select both Patient and Doctor")
    else:
        c.execute("INSERT INTO appointments(patient_id, doctor_id, date, time) VALUES (?,?,?,?)", 
                  (patient_dict[patient_name], doctor_dict[doctor_name], str(date), str(time)))
        conn.commit()
        st.success("Appointment Booked!")


        # menu = ["Add Patient", "Add Doctor", "Book Appointment", "View Data"]
# choice = st.sidebar.selectbox("Menu", menu)

    
   