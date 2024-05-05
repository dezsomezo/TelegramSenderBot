import asyncio
from logic import send_to_all_channels
from settings import manage_users, load_users
import tgcrypto


def select_user(users):
    while True:
        print("Available users:")
        for i, user in enumerate(users):
            print(f"{i}: {user['name']}")
        print(f"{len(users)}: Back")

        user_index = int(input("Select a user by entering their index: "))
        if user_index == len(users):
            return None
        elif 0 <= user_index < len(users):
            return users[user_index]
        else:
            print("Invalid option. Please try again.")


def main():
    while True:
        print("1. Send Message")
        print("2. Settings")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            users = load_users()
            if not users:
                print("No users available. Please add a user first.")
                continue

            selected_user = select_user(users)
            if selected_user is None:
                continue

            message = input("Enter the message to send: ")
            asyncio.run(send_to_all_channels(selected_user, message))

        elif choice == "2":
            manage_users()

        elif choice == "3":
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
