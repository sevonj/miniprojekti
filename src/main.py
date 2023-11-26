"""
main.py

This module is the front for the app.

"""
from pybtex.database import Entry
from app_io import AppIO
from app import App


def print_help(io):
    """UI fn: Help"""
    msg = """M I N I P R O J E K T I
by Ryhmä4

Available commands (case-insensitive):
"""

    # Dic of commands. Key is the command itself and the value is the description.
    commands = {
        "ADD": "Add a new entry to the bibliography",
        "EXIT": "Exit",
        "HELP": "Display this help message",
        "LIST": "Display all entries",
    }

    # Force alphabetical order
    keys = sorted(list(commands.keys()))

    # Figure out how much padding is needed
    maxkeylen = max(len(key) for key in keys)

    for key in keys:
        msg += key.ljust(maxkeylen + 2) + " - " + commands[key] + "\n"

    io.print(msg)


def get_entries(io, app: App):
    """UI fn: Print all entries"""

    io.print(app.get_entries())


def add_entries(io, app: App):
    """UI fn: Add a new entry"""
    io.print("Enter article citation details:")
    author = io.input("Author: ")
    title = io.input("Title: ")
    journal = io.input("Journal: ")
    year = io.input("Year: ")
    volume = io.input("Volume: ")
    number = io.input("Number: ")
    pages = io.input("Pages: ")

    if not any([author, title, journal, year, volume, number, pages]):
        io.print("An entry is missing, try again.")
        return

    # Create an Entry object representing the article citation
    entry = Entry(
        "article",
        fields={
            "author": author,
            "title": title,
            "journal": journal,
            "year": year,
            "volume": volume,
            "number": number,
            "pages": pages,
        },
    )

    # Add the entry to the BibliographyData
    app.add_entry(entry)
    io.print("Entry successfully saved to the database.")


def main(io):
    """Main front"""

    app = App()
    app.create_bib()

    # App loop
    while True:
        command = io.input("Enter command (type HELP for help):\n> ").upper().strip()

        match command:
            case "EXIT":
                break

            case "HELP":
                print_help(io)

            case "ADD":
                add_entries(io, app)

            case "LIST":
                get_entries(io, app)

            case _:
                io.print(f"Unrecognized command: '{command}'")

    # Exit message.
    io.print("Have a nice day.")


if __name__ == "__main__":
    main(AppIO())
