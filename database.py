import sqlite3
import os

DATABASE_FILE = "mental_health_chatbot.db"

def connect_db():
    """Connects to the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        print("Database connection successful.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_tables():
    """Creates the Users and Chat History tables if they don't exist."""
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ChatHistory (
                    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES Users(user_id),
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_message TEXT,
                    bot_response TEXT
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Tables created or already exist.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

def insert_chat_message(user_id, user_message, bot_response):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            print(f"Inserting chat message for user {user_id}: {user_message}")
            cur.execute("""
                INSERT INTO ChatHistory (user_id, user_message, bot_response)
                VALUES (?, ?, ?);
            """, (user_id, user_message, bot_response))
            conn.commit()
            cur.close()
            conn.close()
            print("Chat message inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting chat message: {e}")

def get_chat_history(user_id):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            print(f"Retrieving chat history for user {user_id}")
            cur.execute("""
                SELECT timestamp, user_message, bot_response
                FROM ChatHistory
                WHERE user_id = ?
                ORDER BY timestamp;
            """, (user_id,))
            history = cur.fetchall()
            cur.close()
            conn.close()
            print(f"Chat history retrieved: {history}")
            return history
        except sqlite3.Error as e:
            print(f"Error retrieving chat history: {e}")
            return []

def get_user_password(username):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            print(f"Retrieving password hash for user: {username}")
            cur.execute("""
                SELECT password_hash
                FROM Users
                WHERE username = ?;
            """, (username,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                print("Password hash found.")
                return result[0]
            else:
                print("Password hash not found.")
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving user password: {e}")
            return None

def create_user(username, password_hash):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            print(f"Creating user: {username}")
            cur.execute("""
                INSERT INTO Users (username, password_hash)
                VALUES (?, ?);
            """, (username, password_hash))
            conn.commit()
            cur.close()
            conn.close()
            print(f"User {username} created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")

def get_user_id(username):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            print(f"Retrieving user ID for: {username}")
            cur.execute("""
                SELECT user_id
                FROM Users
                WHERE username = ?;
            """, (username,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                print(f"User ID found: {result[0]}")
                return result[0]
            else:
                print("User ID not found.")
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving user ID: {e}")
            return None
# Call create_tables() to create tables if they don't exist.
if __name__ == "__main__":
    create_tables()
    print("Database setup complete.")