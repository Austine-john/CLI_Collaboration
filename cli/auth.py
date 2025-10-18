# cli/auth.py
from models.user import User

def register():
    print(" Register ")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        return None

    # Create a new user
    user = User.register(username, password)
    if user:
        print(f"User '{username}' registered successfully.")
        return user
    else:
        print("Username already exists. Try a different one.")
        return None


def login():
    print("\n=== Login ===")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Both fields are required.")
        return None

    # Attempt login
    user = User.login(username, password)
    if user:
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Invalid username or password.")
        return None
