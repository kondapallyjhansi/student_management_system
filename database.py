import sqlite3

def connect_db():
    return sqlite3.connect("attendance.db", check_same_thread=False)

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Students Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    # Attendance Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            student_id TEXT,
            date TEXT,
            status TEXT,
            UNIQUE(student_id, date)
        )
    """)

    # Users Table (for login/register)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
