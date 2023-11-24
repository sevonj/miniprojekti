"""
main.py

This module is the front for the app.

"""
from pybtex.database import Entry
from app import App


def print_help():
    """UI fn: Help"""
    titlemessage = """M I N I P R O J E K T I
by Ryhmä4
All commands are case insensitive. Arguments may not be.

Available commands:"""

    # Dic of commands. Key is the command itself and the value is the description.
    commands = {
        "ADD": "Add a new entry to the bibliography",
        "EXIT": "Exit app",
        "LIST": "Show all entries",
    }

    # Force alphabetical order
    keys = sorted(list(commands.keys()))

    # Figure out how much padding is needed
    maxkeylen = max(len(key) for key in keys)

    print(titlemessage)
    for key in keys:
        print(key.ljust(maxkeylen + 2), "-", commands[key])


def get_entries(app: App):
    """UI fn: Print all entries"""
    print(app.get_entries())


def add_entries(app: App):
    """UI fn: Add a new entry"""
    print("Enter article citation details:")
    author = input("Author: ")
    title = input("Title: ")
    journal = input("Journal: ")
    year = input("Year: ")
    volume = input("Volume: ")
    number = input("Number: ")
    pages = input("Pages: ")

    if not any([author, title, journal, year, volume, number, pages]):
        print("An entry is missing, try again.")
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
    print("Entry successfully saved to the database.")


def main():
    """Main front"""
    app = App()
    app.create_bib()

    # App loop
    while True:
        command = input("Enter command (type HELP for help): ").upper().strip()

        match command:
            case "EXIT":
                break

            case "HELP":
                print_help()

            case "ADD":
                add_entries(app)

            case "LIST":
                get_entries(app)

            case _:
                print(f"Unrecognized command: '{command}'")

    # Exit message.
    print("Have a nice day.")


if __name__ == "__main__":
    main()
