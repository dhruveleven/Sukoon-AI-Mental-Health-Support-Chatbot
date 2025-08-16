import sqlite3
from passlib.hash import bcrypt
import re

DATABASE = '../database.db'

def connect_db():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def register_user(username, password):
    if not is_password_strong(password):
        raise ValueError("Password does not meet strength requirements.")
    hashed_password = bcrypt.hash(password)
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            cur.close()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error registering user: {e}")

def verify_user(username, password):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT password FROM Users WHERE username = ?", (username,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                return bcrypt.verify(password, result[0])
            else:
                return False
        except sqlite3.Error as e:
            print(f"Error verifying user: {e}")
            return False

def get_user_id(username):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM Users WHERE username = ?", (username,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting user ID: {e}")
            return None

def is_password_strong(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True