"""
ui.py

This module has the CLI UI functions for the app.

"""
from textwrap import dedent
import re
from os.path import realpath
from pybtex.database import Entry, Person, PybtexError
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
        "DOI": "Search online for an entry by DOI",
        "EXIT": "Exit",
        "HELP": "Display this help message",
        "LIST": "Display all entries",
        "SEARCH": "Search for an entry by title",
        "SAVE": "Save entries to a .bib-file. Overwrites data",
        "LOAD": "Loads entries from a .bib-file",
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


def add_entry(io, app: App):
    """UI fn: Add a new entry"""
    io.print("Enter article citation details:")
    author = io.input("Author: ")
    title = io.input("Title: ")
    journal = io.input("Journal: ")
    year = io.input("Year: ")
    volume = io.input("Volume: ")
    number = io.input("Number: ")
    pages = io.input("Pages: ")

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

    # Add the entry to the Bibliography
    err = app.add_entry(entry)
    if err is None:
        io.print("Entry successfully added to the database.")
    else:
        print(err)


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

    io.print(app.tabulate_entries(entries))

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


def save_entries(io, app: App):
    """UI fn for saving entries to a .bib-file"""
    path = realpath("./bib_export.bib")
    reply = io.input("Enter file name, e.g. export or export.bib [bib_export.bib] ")
    if reply:
        path = realpath(f"./{reply if reply.endswith('.bib') else reply +'.bib'}")

    try:
        app.save_to_file(path)
        io.print(f"Saved to {path}")
    except PybtexError:
        io.print("\n\tSaving file failed. Try another file name\n")


def load_entries(io, app: App):
    """UI fn for loading entries from a .bib-file"""

    path = realpath("./bib_export.bib")

    reply = io.input("Enter file name, e.g. export or export.bib [bib_export.bib] ")
    if reply:
        path = realpath(f"./{reply if reply.endswith('.bib') else reply +'.bib'}")

    try:
        app.load_from_file(path)
        io.print(f"Loaded from {path}")
    except PybtexError:
        io.print("\n\tLoading file failed. Try another file name\n")


def search_doi(io, app: App):
    """UI fn: Search for an entry"""
    doi = io.input("Search: Enter DOI of the citation: ")
    if not doi:
        io.print("DOI is missing, search cancelled.")
        return
    search_result = app.get_bibtex_by_doi(doi)
    if search_result.startswith(" @"):
        entry = app.parse_entry_from_bibtex(search_result)
        temp_dict = {doi: entry}
        io.print(app.tabulate_entries(temp_dict))
        confirm_add = io.input(
            "Entry successfully retrieved. Would you like to add it to bibliography? y/N:"
        )
        if confirm_add.upper().strip() == "Y":
            app.add_entry(entry)
            io.print("Entry successfully saved to the database.")
        else:
            io.print("Entry not added.")
            return
    else:
        io.print(search_result)
