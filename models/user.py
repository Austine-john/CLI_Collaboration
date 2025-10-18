# models/user.py
import sqlite3
from db import get_connection

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def create(cls, username, password):
        """Register a new user."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            print(f" User '{username}' registered successfully!")
        except sqlite3.IntegrityError:
            print(f"Username '{username}' already exists.")
        finally:
            conn.close()

    @classmethod
    def login(cls, username, password):
        """Authenticate user credentials."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            print(f"Welcome back, {username}!")
            return cls(*row)
        else:
            print("Invalid username or password.")
            return None

    @classmethod
    def all(cls):
        """List all registered users."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users")
        users = [cls(*row) for row in cursor.fetchall()]
        conn.close()
        return users

    def __repr__(self):
        return f"<User {self.username}>"
