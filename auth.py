from database import connect_db

# Register User
def register(username, password):
    conn = connect_db()
    cur = conn.cursor()

    # Check if username exists
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    if cur.fetchone():
        conn.close()
        return False  # Already exists

    cur.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username, password)
    )
    conn.commit()
    conn.close()
    return True


# Login User
def login(username, password):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()
    conn.close()

    return user is not None
