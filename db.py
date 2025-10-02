import sqlite3

def create_connection():
    conn = sqlite3.connect("mydb.db", check_same_thread=False)
    return conn

conn = create_connection()
cursor = conn.cursor()

def reg(data):
    try:
        cursor.execute(
            '''INSERT INTO Feedback (name, email, feedback) VALUES (?, ?, ?)''',
            data
        )
        conn.commit()
        print("Thank you for your feedback")
        return True
    except sqlite3.Error as e:
        print("Error:", e)
        return False

def view():
    try:
        cursor.execute("SELECT * FROM Feedback")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error:", e)
        return []
