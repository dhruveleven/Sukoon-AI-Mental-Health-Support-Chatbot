from passlib.hash import bcrypt
import database

def register_user(username, password):
    print(f"Registering user: {username}")
    password_hash = bcrypt.hash(password)
    database.create_user(username, password_hash)
    print(f"User {username} registered.")

def verify_user(username, password):
    print(f"Verifying user: {username}")
    stored_hash = database.get_user_password(username)
    if stored_hash:
        print("Stored hash found.")
        return bcrypt.verify(password, stored_hash)
    print("Stored hash not found.")
    return False

def get_user_id(username):
    print(f"Getting user id for: {username}")
    return database.get_user_id(username)