"""
app.py

This module contains the service which the UI code can call.
It should be kept UI-independent; No UI code here.

"""
from uuid import uuid4
from pybtex.database import BibliographyData, Entry
from tabulate import tabulate


class App:
    """
    Application class
    UI-agnostic Application logic.
    """

    def __init__(self):
        self._bib_data = None

    def create_bib(self):
        """Load an empty bibliography"""
        self._bib_data = BibliographyData()

    def get_entries(self):
        """Get the entries from the bibliography

        Returns:
            entries: the entries from the bibliography
            message: a message describing the result of the operation
        """
        try:
            if not self._bib_data.entries:
                return None, "No entries found"

            return self._bib_data.entries, "Successfully retrieved entries"

        except Exception as e:  # pylint: disable=broad-except
            return None, f"Failed to retrieve entries: {e}"

    def add_entry(self, entry: Entry):
        """
        params:
            entry: this will be added
        """
        key = str(uuid4())
        self._bib_data.add_entry(key, entry)

    def del_entries(self, entry_indices: list[int]):
        """Deletes select entries, or all.

        Args:
            entry_indices (list): the indices of stringkeys of entries to delete.
                                  An empty list defaults to deleting all entries.
        """

        # getting ALL keys first, avoiding "mutation during iteration"
        keys = list(self._bib_data.entries)

        # try/catch removed, entry_indices are sanitized in main.py
        # deleting specific entries from the `entries` arg
        if len(entry_indices) > 0:
            for idx in entry_indices:
                del self._bib_data.entries[keys[idx]]
            return

        for key in keys:
            del self._bib_data.entries[key]

    def tabulate_entries(self, entries):
        """Create a table of bibliography entries using the tabulate library

        Args:
            entries: A list of pybtex Entry objects
        Returns:
            A string containing a table of bibliography entries
        """
        table_data = []
        for key, entry in entries.items():
            authors = " and ".join(
                str(person) for person in entry.persons.get("author", [])
            )
            title = entry.fields.get("title", "N/A")
            journal = entry.fields.get(
                "journal", entry.fields.get("publisher", "N/A"))
            year = entry.fields.get("year", "N/A")

            table_data.append([key, authors, title, journal, year])

        return tabulate(
            table_data, headers=["Citekey",
                                 "Author", "Title", "Journal", "Year"]
        )

    def find_entries_by_title(self, searched):
        """Find all entries where searched word is included the title.

        Args:
            searched: A string, a part of title of the searched entry
        Returns:
            A dictionary of pybtex Entry objects
        """

        filtered_entries = {}
        for citekey, entry in self.get_entries()[0].items():
            if (
                "title" in entry.fields
                and searched.lower() in entry.fields["title"].lower()
            ):
                filtered_entries[citekey] = entry

        return filtered_entries
