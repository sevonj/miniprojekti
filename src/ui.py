"""
ui.py

This module has the CLI UI functions for the app.

"""
from textwrap import dedent
import re
from os.path import realpath
from pybtex.database import Entry, Person, PybtexError
from tabulate import tabulate
from app import App

DEFAULT_FIELDS = ["citekey", "author", "title", "journal", "year"]
DEFAULT_LIMIT = 40


def format_entries(entries: list, fields=None) -> list:
    """Makes entries into a friendlier for further use, such as tabulate.

    Args:
        entries (list): List of entries
        fields (list[str]): (optional) (case-insensitive):
            Choose specific fields for the output. Leave out for `DEFAULT_ENTRIES`.
            Example: ["idx", "citekey", "Author", "YEAR", "nonexistent-field"]

    Returns:
        entries (list[dict]): Entries are dicts. Keys are field names and capitalized.
    """
    ret_entries = []
    for idx, (citekey, entry) in enumerate(entries.items()):
        entrydict = {}

        # No custom field keys given. Return citekey + all fields
        if fields is None:
            entrydict["citekey"] = citekey  # Citekey
            entrydict["author"] = format_authors(entry.persons.get("author", []))
            for field in entry.fields:  # Get all fields
                if field.lower() == "title":
                    entrydict["title"] = limit_str_len(entry.fields.get(field, "N/A"))
                    continue
                entrydict[field.capitalize()] = entry.fields.get(field, "N/A")

        # Custom field keys were given. Return whichever fields were asked.
        else:
            for field in fields:
                if field.lower() == "idx":
                    entrydict["Idx"] = idx
                    continue
                if field.lower() == "citekey":
                    entrydict["Citekey"] = citekey
                    continue
                if field.lower() == "author":
                    entrydict["Author"] = format_authors(
                        entry.persons.get("author", [])
                    )
                    continue
                if field.lower() == "title":
                    entrydict["Title"] = limit_str_len(entry.fields.get(field, "N/A"))
                    continue
                entrydict[field.capitalize()] = entry.fields.get(field, "N/A")

        ret_entries.append(entrydict)

    return ret_entries


def limit_str_len(string: str, limit=DEFAULT_LIMIT) -> str:
    """Limits the length of a string to a given limit.
    Args:
        string (str): The string to be limited
        limit (int): The limit of the string length

    Returns:
        str: The limited string
    """
    if len(string) > limit:
        return string[:limit] + "..."
    return string


def format_authors(authors):
    """
    Format a list of authors to Author et al if over 3 authors
    params: list of Person objects
    Returns: string of formatted authors
    """
    if len(authors) > 3:
        return f"{authors[0]} et al."

    authorstring = f"{authors[0]}"
    for i in range(1, len(authors)):
        authorstring += f" and {authors[i]}"
    return authorstring


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
    entries = app.get_entries()[0]

    if entries is None or len(entries) == 0:
        io.print("No entries found.")
        return

    io.print("Succesfully retrieved entries:\n")
    io.print(
        tabulate(
            format_entries(entries, DEFAULT_FIELDS),
            headers="keys",
        ),
        "\n",
    )


def add_entry(io, app: App):
    """UI fn: Add a new entry"""
    io.print("Enter article citation details:")

    fieldstoask = [
        "author",
        "title",
        "journal",
        "year",
        "volume",
        "number",
        "pages",
    ]
    authors = ""
    fields = {}
    for field in fieldstoask:
        prompt = field.capitalize() + ": "
        value = io.input(prompt)

        # Force required
        if field in {"author", "title"}:
            while value == "":
                value = io.input("This field is required!\n" + prompt)

        # Author isn't a normal field
        if field == "author":
            authors = value
            continue

        if value != "":
            fields[field] = value

    # Create an Entry object representing the article citation
    entry = Entry(
        "article",
        persons={"author": [Person(name) for name in authors.split(" and ")]},
        fields=fields,
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
    io.print(
        tabulate(
            format_entries(filtered_entries, DEFAULT_FIELDS),
            headers="keys",
        ),
        "\n",
    )


re_idx = re.compile(r"\S+")


def del_entries(io, app: App):
    """UI fn: delete one or more entries."""

    entries = app.get_entries()[0]
    if not entries:
        io.print("there is nothing to delete")
        return

    valid_index_range = range(len(entries))
    indices_to_remove = set()

    io.print(
        tabulate(
            format_entries(entries, ["idx"] + DEFAULT_FIELDS),
            headers="keys",
        ),
        "\n",
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

    success, search_result = app.get_bibtex_by_doi(doi)

    if success and search_result.startswith(" @"):
        success, entry = app.parse_entry_from_bibtex(search_result)
        if success:
            citekey = app.generate_citekey(entry)
            io.print(
                tabulate(
                    format_entries({citekey: entry}, DEFAULT_FIELDS),
                    headers="keys",
                ),
                "\n",
            )
            confirm_add = io.input(
                "\nEntry successfully retrieved. Would you like to add it to bibliography? y/N:"
            )
            if confirm_add.upper().strip() == "Y":
                app.add_entry(entry)
                io.print("\nEntry successfully saved to the database.\n")
            else:
                io.print("\nEntry not added.\n")
                return
        else:
            io.print(entry)
    else:
        io.print(search_result)
