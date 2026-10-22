"""Simple local role login using JSON file handling and password hashes."""
import hashlib
import hmac
import os
from getpass import getpass
from storage import load_json, save_json
from utils import choose, text_input


def password_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                              bytes.fromhex(salt), 150000).hex()


def ask_password(label):
    try:
        return getpass(label)
    except (EOFError, KeyboardInterrupt):
        raise


def make_account(username, password, role):
    salt = os.urandom(16).hex()
    return {"username": username, "role": role, "salt": salt,
            "password_hash": password_hash(password, salt)}


def setup_admin():
    if load_json("users"):
        return
    print("FIRST-TIME SETUP: Create an administrator account")
    username = text_input("Admin username: ")
    while True:
        password = ask_password("Admin password (minimum 6 characters): ")
        if len(password) >= 6:
            break
        print("Password must contain at least 6 characters.")
    save_json("users", [make_account(username, password, "admin")])
    print("Administrator account created.")


def login():
    users = load_json("users")
    for attempt in range(3):
        username = text_input("Username: ")
        password = ask_password("Password: ")
        for user in users:
            if user["username"] == username and hmac.compare_digest(
                    user["password_hash"], password_hash(password, user["salt"])):
                print("Logged in as", user["username"], "(" + user["role"] + ")")
                return user
        print("Incorrect username or password.")
    print("Too many failed attempts.")
    return None


def manage_users():
    while True:
        choice = choose("ADMIN - USER MANAGEMENT", ["Add staff user", "View user accounts", "Back"])
        if choice == 3:
            return
        users = load_json("users")
        if choice == 2:
            for user in users:
                print("Username:", user["username"], "| Role:", user["role"])
            continue
        username = text_input("New staff username: ")
        if any(user["username"].casefold() == username.casefold() for user in users):
            print("Username already exists.")
            continue
        while True:
            password = ask_password("New password (minimum 6 characters): ")
            if len(password) >= 6:
                break
            print("Password must contain at least 6 characters.")
        users.append(make_account(username, password, "staff"))
        save_json("users", users)
        print("Staff account created.")
