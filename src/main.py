"""
main.py

This module is the front for the app.

"""
from pybtex.database import Entry
from app_io import AppIO
from app import App


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


def main(io=None):
    """Main front"""

    app = App()
    app.create_bib()

    # App loop
    while True:
        command = io.input("Enter command (ADD/LIST/EXIT): ").upper().strip()

        match command:
            case "EXIT":
                break

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
