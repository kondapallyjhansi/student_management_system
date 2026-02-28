import pandas as pd
from database import connect_db
import streamlit as st

def show_dashboard(st):

    conn = connect_db()

    students = pd.read_sql("SELECT * FROM students", conn)
    attendance = pd.read_sql("SELECT * FROM attendance", conn)

    st.subheader("📊 Attendance Dashboard")

    if attendance.empty:
        st.warning("No attendance records found")
        return

    present_count = len(attendance[attendance['status'] == "Present"])
    absent_count = len(attendance[attendance['status'] == "Absent"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", len(students))
    col2.metric("Present", present_count)
    col3.metric("Absent", absent_count)

    st.write("### Attendance Records")
    st.dataframe(attendance)

    conn.close()
