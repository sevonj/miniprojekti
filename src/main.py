"""
main.py

This module is the front for the app.

"""
from textwrap import dedent
import re
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


re_idx = re.compile(r"\S+")


def del_entries(io, app: App):
    """UI fn: delete one or more entries."""

    entries = app.get_entries()[0]
    if not entries:
        io.print("there is nothing to delete")
        return

    valid_index_range = range(len(entries))
    indices_to_remove = []

    # pretty formatting here
    # prolly simply call the listing function once done with the addition of indices
    io.print(
        f"\n{'ID':^3} | {'author':^10} | {'title':^10} | {'journal':^10} | {'year':^10}")
    for idx, (_entry_key, entry) in enumerate(entries.items()):
        fields = entry.fields
        io.print(
            f"{idx:^3} | {fields['author']:^10} | {fields['title']:^10} "
            + f"| {fields['journal']:^10} | {fields['year']:^10}"
        )

    reply = io.input(dedent(
        """
        Which entries do you want to remove? Type either:
        - indeces separated by whitespace, e.g. '0 1 5'
        - or the word 'ALL' to remove all entries:

        [none]: """
    )).upper().strip()

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
                indices_to_remove.append(idx)

            except ValueError:
                io.print(f"\n\tERROR: unrecognized index: {idx_as_str}\n")
                return

    confirm = io.input(
        "Are you sure you want to delete "
        + (
            '*ALL* entries' if reply == 'ALL' else
            f'entries with row numbers ({"".join(indices_to_remove)})'
        )
        + "? [y/N]: "
    ).upper().strip()

    if len(confirm) == 0 or confirm[0] != "Y":
        io.print("deletion of entries cancelled")
        return

    app.del_entries(indices_to_remove)


def main(io=None):
    """Main front"""

    app = App()
    app.create_bib()

    # App loop
    while True:
        command = io.input(
            "Enter command (ADD/LIST/DELETE/EXIT): "
        ).upper().strip()

        match command:
            case "EXIT":
                break

            case "ADD":
                add_entries(io, app)

            case "DELETE":
                del_entries(io, app)

            case "LIST":
                get_entries(io, app)

            case _:
                io.print(f"Unrecognized command: '{command}'")

    # Exit message.
    io.print("Have a nice day.")


if __name__ == "__main__":
    main(AppIO())
