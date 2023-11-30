"""
main.py

This module is the front for the app.

"""
from textwrap import dedent
import re
from pybtex.database import Entry, Person
from app_io import AppIO
from app import App
from os.path import realpath


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
        "EXPORT": "Export entries to a .bib-file. Overwrites data",
        "IMPORT": "Imports entries from default .bib-file",
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
    # Check if there are any entries and print infomessage is there are none
    if app.get_entries()[0] is None:
        io.print(app.get_entries()[1])
        return

    # Get entries and print tabulated form
    io.print(app.tabulate_entries(app.get_entries()[0]))

    # Print infomessage when successfully retrieved entries
    io.print(app.get_entries()[1])


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
    filtered_entries = app.find_entries_by_title(search)
    io.print(app.tabulate_entries(filtered_entries))


re_idx = re.compile(r"\S+")


def del_entries(io, app: App):
    """UI fn: delete one or more entries."""

    entries = app.get_entries()[0]
    if not entries:
        io.print("there is nothing to delete")
        return

    valid_index_range = range(len(entries))
    indices_to_remove = set()

    # pretty formatting here
    # prolly simply call the listing function once done with the addition of indices
    io.print(
        f"\n{'ID':^3} | {'author':^10} | {'title':^10} | {'journal':^10} | {'year':^10}"
    )
    for idx, (_entry_key, entry) in enumerate(entries.items()):
        fields = entry.fields
        person = entry.persons
        author = ",".join([str(x) for x in person["author"]])
        io.print(
            f"{idx:^3} | {author:^10} | {fields['title']:^10} "
            + f"| {fields['journal']:^10} | {fields['year']:^10}"
        )

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


def export_entries(io, app: App):
    """UI fn for exporting entries to a default .bib-file"""

    path = realpath("./bib_export.bib")
    app.save_to_file(path)
    io.print(f"Exported to {path}")


def import_entries(io, app: App):
    """UI fn for importing entries from a default .bib-file"""

    path = realpath("./bib_export.bib")
    app.load_from_file(path)
    io.print(f"Imported from {path}")


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

            case "EXPORT":
                export_entries(io, app)

            case "IMPORT":
                import_entries(io, app)

            case _:
                io.print(f"Unrecognized command: '{command}'")

    # Exit message.
    io.print("Have a nice day.")


if __name__ == "__main__":
    main(AppIO())
