"""
main.py

This module is the front for the app.

"""
from textwrap import dedent
import re
from pybtex.database import Entry, Person
from tabulate import tabulate
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
        "DELETE": "Delete one or more entries",
        "EXIT": "Exit",
        "HELP": "Display this help message",
        "LIST": "Display all entries",
        "SEARCH": "Search for an entry by title",
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

    # Print infomessage
    io.print("\n", app.get_entries()[1])

    # No entries, return
    if app.get_entries()[0] is None:
        return

    entries = app.get_entries()[0]
    table_data = []
    for key, entry in entries.items():
        authors = ", ".join(str(person) for person in entry.persons.get("author", []))
        title = entry.fields.get("title", "N/A")
        journal = entry.fields.get("journal", entry.fields.get("publisher", "N/A"))
        year = entry.fields.get("year", "N/A")
        table_data.append([key, authors, title, journal, year])

    io.print(
        tabulate(table_data, headers=["Citekey", "Author", "Title", "Journal", "Year"]),
        "\n",
    )


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
        persons={"author": [Person(name) for name in author.split(" and ")]},
        fields={
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


def search_entries(io, app: App):
    """UI fn: Search for an entry"""
    search = io.input("Search: Enter title of the citation: ")
    entries = app.find_entries_by_title(search)

    table_data = []
    for key, entry in entries.items():
        authors = ", ".join(str(person) for person in entry.persons.get("author", []))
        title = entry.fields.get("title", "N/A")
        journal = entry.fields.get("journal", entry.fields.get("publisher", "N/A"))
        year = entry.fields.get("year", "N/A")
        table_data.append([key, authors, title, journal, year])

    io.print(
        tabulate(table_data, headers=["Citekey", "Author", "Title", "Journal", "Year"]),
        "\n",
    )


def format_names(names: []) -> str:
    """
    Param: Array of names
    Return: Names formatted into one string
    """
    return ", ".join(str(person) for person in names)


re_idx = re.compile(r"\S+")


def del_entries(io, app: App):
    """UI fn: delete one or more entries."""

    entries = app.get_entries()[0]
    if not entries:
        io.print("there is nothing to delete")
        return

    table_data = [
        {
            "Idx": i,
            "Citekey": key,
            "Author": format_names(entry.persons.get("author", [])),
            "Title": entry.fields.get("title", "N/A"),
            "Journal": (
                entry.fields.get("journal", entry.fields.get("publisher", "N/A"))
            ),
            "Year": entry.fields.get("year", "N/A"),
        }
        for i, (key, entry) in enumerate(entries.items())
    ]

    io.print(tabulate(table_data, headers="keys"))

    valid_index_range = range(len(entries))
    indices_to_remove = set()

    reply = (
        io.input(
            dedent(
                """
        Which entries do you want to remove? Type either:
        - indeces separated by whitespace, e.g. '0 1 5'
        - or the word 'ALL' to remove all entries:

        [none]: """
            )
        )
        .upper()
        .strip()
    )

    # not deleting anything
    if reply == "":
        io.print("deletion of entries cancelled")
        return

    if reply != "ALL":
        for idx_as_str in re_idx.findall(reply):
            try:
                idx = int(idx_as_str)
                if idx not in valid_index_range:
                    io.print(f"\n\tERROR: out-of-bounds index: {idx}\n")
                    return
                indices_to_remove.add(idx)

            except ValueError:
                io.print(f"\n\tERROR: unrecognized index: {idx_as_str}\n")
                return

    confirm = (
        io.input(
            "Are you sure you want to delete "
            + (
                "*ALL* entries"
                if reply == "ALL"
                else f"entries with row numbers ({list(indices_to_remove)})"
            )
            + "? [y/N]: "
        )
        .upper()
        .strip()
    )

    if len(confirm) == 0 or confirm[0] != "Y":
        io.print("deletion of entries cancelled")
        return

    app.del_entries(list(indices_to_remove))


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

            case "DELETE":
                del_entries(io, app)

            case "LIST":
                get_entries(io, app)

            case "SEARCH":
                search_entries(io, app)

            case _:
                io.print(f"Unrecognized command: '{command}'")

    # Exit message.
    io.print("Have a nice day.")


if __name__ == "__main__":
    main(AppIO())
