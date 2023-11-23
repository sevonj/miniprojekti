"""
main.py

This module is the front for the app.

"""
from pybtex.database import Entry
from app import App


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
        command = input("Enter command (ADD/LIST/EXIT): ").upper().strip()

        match command:
            case "EXIT":
                break

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
