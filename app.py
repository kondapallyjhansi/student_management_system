import streamlit as st
from database import create_tables, connect_db
from auth import login
from dashboard import show_dashboard
import pandas as pd
from datetime import date

st.set_page_config(page_title="Attendance System", layout="wide")
create_tables()

st.title("🎓 Smart Attendance Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Add Student", "Mark Attendance", "Dashboard"]
)

# ---------- LOGIN ----------
if menu == "Login":

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(user, pwd):
            st.success("Login Successful")
        else:
            st.error("Invalid Login")


# ---------- ADD STUDENT ----------
elif menu == "Add Student":

    st.subheader("Add New Student")

    student_id = st.text_input("Student ID")
    name = st.text_input("Student Name")

    if st.button("Add Student"):

        if student_id.strip() == "" or name.strip() == "":
            st.warning("Please fill all fields")

        else:
            conn = connect_db()
            cur = conn.cursor()

            # Check duplicate
            cur.execute(
                "SELECT * FROM students WHERE student_id=?",
                (student_id,)
            )

            existing = cur.fetchone()

            if existing:
                st.error("Student ID already exists ❌")
            else:
                cur.execute(
                    "INSERT INTO students(student_id,name) VALUES(?,?)",
                    (student_id, name)
                )
                conn.commit()
                st.success("Student Added Successfully ✅")

            conn.close()


# ---------- MARK ATTENDANCE ----------
elif menu == "Mark Attendance":

    conn = connect_db()
    students = pd.read_sql("SELECT * FROM students", conn)

    if students.empty:
        st.warning("No students found. Add students first.")
    else:
        today = str(date.today())
        st.subheader(f"Mark Attendance - {today}")

        for index, row in students.iterrows():

            status = st.selectbox(
                f"{row['student_id']} - {row['name']}",
                ["Present", "Absent"],
                key=f"status_{row['student_id']}"
            )

            if st.button(
                f"Save {row['student_id']}",
                key=f"save_{row['student_id']}"
            ):
                try:
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO attendance VALUES(?,?,?)",
                        (row['student_id'], today, status)
                    )
                    conn.commit()
                    st.success("Attendance Saved ✅")
                except:
                    st.warning("Attendance already marked for today ⚠️")

        conn.close()


# ---------- DASHBOARD ----------
elif menu == "Dashboard":
    show_dashboard(st)
