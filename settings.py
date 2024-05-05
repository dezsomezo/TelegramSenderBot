import json
import os
import asyncio
from pyrogram import Client, errors

SESSION_DIR = "sessions"


def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


async def create_session(user):
    session_path = os.path.join(SESSION_DIR, user['name'])
    async with Client(session_path, user['api_id'], user['api_hash'], phone_number=user['phone_number']) as client:
        if not client.is_connected:
            try:
                await client.start()
            except errors.SessionPasswordNeeded:
                password = input("Two-step verification enabled. Please enter your password: ")
                await client.start(password=password)
        print("Session created successfully.")


def add_user(users):
    name = input("Enter name: ")
    api_id = int(input("Enter API ID: "))
    api_hash = input("Enter API hash: ")
    phone_number = input("Enter phone number (with country code): ")
    user = {"name": name, "api_id": api_id, "api_hash": api_hash, "phone_number": phone_number}
    users.append(user)
    save_users(users)
    os.makedirs(SESSION_DIR, exist_ok=True)
    asyncio.run(create_session(user))
    print("User added successfully.")


def remove_user(users):
    while True:
        print("Available users:")
        for i, user in enumerate(users):
            print(f"{i}: {user['name']}")
        print(f"{len(users)}: Back")

        user_index = int(input("Select a user to remove by entering their index: "))
        if user_index == len(users):
            return
        elif 0 <= user_index < len(users):
            user = users.pop(user_index)
            save_users(users)
            session_path = os.path.join(SESSION_DIR, user['name'])
            try:
                os.remove(session_path + ".session")
                os.remove(session_path + ".session-journal")
            except FileNotFoundError:
                pass
            print("User removed successfully.")
            return
        else:
            print("Invalid option. Please try again.")


def manage_users():
    users = load_users()
    while True:
        print("1. Add User")
        print("2. Remove User")
        print("3. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == "1":
            add_user(users)
        elif choice == "2":
            remove_user(users)
        elif choice == "3":
            break
        else:
            print("Invalid option. Please try again.")
