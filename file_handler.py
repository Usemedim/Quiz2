import json
import os
from datetime import datetime

USERS_FILE = "users.json"

def load_users():
    """Load users from the JSON file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_users(users):
    """Save users to the JSON file."""
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

def find_or_create_user(email, name):
    """Find a user by email or create a new one."""
    users = load_users()
    user = next((u for u in users if u["email"] == email), None)
    if user is None:
        user = {
            "name": name,
            "email": email,
            "registration_date": datetime.now().strftime("%Y-%m-%d"),
            "history": []
        }
        users.append(user)
        save_users(users)
    return user
