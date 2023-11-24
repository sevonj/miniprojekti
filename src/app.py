"""
app.py

This module contains the service which the UI code can call.
It should be kept UI-independent; No UI code here.

"""
from pybtex.database import BibliographyData, Entry


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
            entries = self._bib_data.entries

            if not entries:
                return None, "No entries found"

            for _, entry in entries.items():
                print(entry.to_string("bibtex"))
            return (entries, "Successfully retrieved entries")

        except Exception as e:  # pylint: disable=broad-except
            return None, f"Failed to retrieve entries: {e}"

    def add_entry(self, entry: Entry):
        """
        params:
            entry: this will be added
        """
        key = str(len(self._bib_data.entries))
        self._bib_data.add_entry(key, entry)
