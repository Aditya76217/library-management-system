"""
auth.py - Simple authentication module for the Library Management System.
Stores credentials in a JSON file with hashed passwords.
"""

import json
import os
import hashlib


AUTH_FILE = os.path.join("data", "users.json")

# Default admin credentials (username: admin, password: admin123)
DEFAULT_USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "librarian": hashlib.sha256("lib2024".encode()).hexdigest(),
}


def _ensure_auth_file():
    """Create auth file with default users if it doesn't exist."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_USERS, f, indent=2)


def _load_users() -> dict:
    """Load user credentials from file."""
    _ensure_auth_file()
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def authenticate(username: str, password: str) -> bool:
    """
    Validate username/password.
    Returns True if credentials are correct.
    """
    users = _load_users()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return users.get(username) == hashed
