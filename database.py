import sqlite3

def connect_db():
    return sqlite3.connect("attendance.db", check_same_thread=False)

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Students Table (Student ID UNIQUE)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    # Attendance Table (No duplicate per day)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            student_id TEXT,
            date TEXT,
            status TEXT,
            UNIQUE(student_id, date)
        )
    """)

    # Users Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    # Default Admin
    cur.execute("INSERT OR IGNORE INTO users VALUES('admin','admin123')")

    conn.commit()
    conn.close()
