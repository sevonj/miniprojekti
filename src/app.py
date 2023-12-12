"""
app.py

This module contains the service which the UI code can call.
It should be kept UI-independent; No UI code here.

"""
from uuid import uuid4
import urllib.request
from urllib.error import HTTPError
from pybtex.database import BibliographyData, Entry, parse_string, parse_file

BASE_DOI_URL = "http://dx.doi.org/"


class App:
    """
    Application class
    UI-agnostic Application logic.
    """

    def __init__(self):
        self.file_changed: bool = False
        self._bib_data: BibliographyData = None  # Currently loaded bibliography
        self._bib_path: str = None  # Filepath of currently loaded biblography

    def set_bib_path(self, path: str) -> None:
        """
        Store filepath of currently loaded bibgliography
        None is an acceptable value.
        """
        self._bib_path = path

    def get_bib_path(self) -> str | None:
        """
        Get filepath of currently loaded bibgliography
        Return value may be None
        """
        return self._bib_path

    def create_bib(self):
        """Load an empty bibliography"""
        self._bib_data = BibliographyData()
        self.file_changed = False

    def load_from_file(self, path: str) -> None:
        """
        Warning: Overwrites loaded bibliography without asking.
        params: Filepath to load
        """
        self._bib_data = parse_file(path, "bibtex")
        self.file_changed = False
        self._bib_path = path

    def save_to_file(self, path: str) -> None:
        """
        Warning: Overwrites file without asking.
        params: Filepath to save
        """
        self._bib_data.to_file(path)
        self.file_changed = False

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

    def add_entry(self, entry: Entry) -> None | str:
        """
        params:
            entry: this will be added
        return:
            Error message: None | str
        """
        key = str(uuid4())
        entries = self._bib_data.entries
        title = entry.fields.get("title")

        if entries:
            for _citekey, existing_entry in entries.items():
                existing_title = existing_entry.fields.get("title")
                if existing_title.lower() == title.lower():
                    return "Failed to add the entry: Another entry with this title already exists."

        self._bib_data.add_entry(key, entry)
        self.file_changed = True
        return None

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
                self.file_changed = True
                del self._bib_data.entries[keys[idx]]
            return
        self.file_changed = True
        for key in keys:
            del self._bib_data.entries[key]

    def find_entries_by_title(self, searched):
        """Find all entries where searched word is included the title.

        Args:
            searched: A string, a part of title of the searched entry
        Returns:
            A dictionary of pybtex Entry objects
        """

        filtered_entries = {}
        if self.get_entries()[0] is None:
            return filtered_entries
        for citekey, entry in self.get_entries()[0].items():
            if (
                "title" in entry.fields
                and searched.lower() in entry.fields["title"].lower()
            ):
                filtered_entries[citekey] = entry

        return filtered_entries

    def get_bibtex_by_doi(self, doi, doi_url=BASE_DOI_URL):
        """Get a BibTeX entry by DOI

        Method code follows the idea by christian from: https://scipython.com/blog/doi-to-bibtex/

        Args:
            doi: A DOI string
        Returns:
            A BibTeX entry as a string
        """
        url = doi_url + doi
        req = urllib.request.Request(url)

        # Add header for requesting BibTeX format
        req.add_header("Accept", "application/x-bibtex")

        try:
            with urllib.request.urlopen(req) as f:
                bibtex_entry = f.read().decode()
            return bibtex_entry
        except HTTPError as e:
            if e.code == 404:
                return "DOI not found."
            return "Service unavailable."

    def parse_entry_from_bibtex(self, bibtex_entry):
        """Parse a BibTeX entry

        Args:
            bibtex_entry: A BibTeX entry as a string
        Returns:
            A pybtex Entry object
        """
        bib_data = parse_string(bibtex_entry, "bibtex")
        return list(bib_data.entries.values())[0]
