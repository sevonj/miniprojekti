"""
main.py

This module is the front for the app.

"""
from app import App


def main():
    app = App()
    app.create_bib()

    # App loop
    while True:
        command = input("Enter command (ADD/LIST/EXIT): ").upper().strip()

        match command:
            case "EXIT":
                break
            case _:
                print(f"Unrecognized command: '{command}'")

    # Exit message.
    print("Have a nice day.")


if __name__ == "__main__":
    main()
