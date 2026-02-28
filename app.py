import streamlit as st
from database import create_tables, connect_db
from auth import login, register
from dashboard import show_dashboard
import pandas as pd
from datetime import date

st.set_page_config(page_title="Attendance System", layout="wide")
create_tables()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🎓 Smart Attendance Management System")

# =========================
# LOGIN / REGISTER PAGE
# =========================
if not st.session_state.logged_in:

    option = st.radio("Select Option", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # -------- LOGIN --------
    if option == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.success("Login Successful ✅")
                st.rerun()
            else:
                st.error("Invalid Credentials ❌")

    # -------- REGISTER --------
    elif option == "Register":
        if st.button("Register"):
            if username.strip() == "" or password.strip() == "":
                st.warning("Please fill all fields")
            else:
                if register(username, password):
                    st.success("Registration Successful ✅ Please Login")
                else:
                    st.error("Username already exists ❌")

# =========================
# MAIN SYSTEM (After Login)
# =========================
else:

    st.sidebar.success("Logged In")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    menu = st.sidebar.selectbox(
        "Menu",
        ["Add Student", "Mark Attendance", "Dashboard"]
    )

    # ---------- ADD STUDENT ----------
    if menu == "Add Student":

        st.subheader("Add New Student")

        student_id = st.text_input("Student ID")
        name = st.text_input("Student Name")

        if st.button("Add Student"):

            if student_id.strip() == "" or name.strip() == "":
                st.warning("Please fill all fields")

            else:
                conn = connect_db()
                cur = conn.cursor()

                cur.execute(
                    "SELECT * FROM students WHERE student_id=?",
                    (student_id,)
                )

                if cur.fetchone():
                    st.error("Student ID already exists ❌")
                else:
                    cur.execute(
                        "INSERT INTO students VALUES(?,?)",
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
            st.warning("No students found.")
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
