from database import connect_db

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
