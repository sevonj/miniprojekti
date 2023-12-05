"""
app_test.py

This module contains unit tests for the App class.

"""
# pylint: disable=protected-access missing-class-docstring missing-function-docstring

import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from pybtex.database import BibliographyData, Entry, Person
from app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.create_bib()
        self.entries = [
            Entry(
                "article",
                persons={"author": [Person("Author1")]},
                fields={"title": "Title1"},
            ),
            Entry(
                "article",
                persons={"author": [Person("Author2")]},
                fields={"title": "Title2"},
            ),
            Entry(
                "article",
                persons={"author": [Person("Author3")]},
                fields={"title": "Title3"},
            ),
        ]

    def test_create_bib(self):
        self.app._bib_data = None
        self.app.create_bib()
        self.assertEqual(self.app._bib_data, BibliographyData())

    def test_add_entry(self):
        entry = Entry(
            "article",
            persons={"author": [Person("Author")]},
            fields={
                "title": "Title",
                "journal": "Journal",
                "year": "Year",
                "volume": "Volume",
                "number": "Number",
                "pages": "Pages",
            },
        )
        # no entries yet
        self.assertEqual(len(self.app._bib_data.entries), 0)

        self.app.add_entry(entry)

        # one entry is added
        self.assertEqual(len(self.app._bib_data.entries), 1)

        # added entry is equal to the original obj
        key = list(self.app._bib_data.entries.keys())[0]
        saved_entry = self.app._bib_data.entries[key]
        self.assertEqual(entry, saved_entry)

    def test_get_entries(self):
        entry = Entry(
            "article",
            persons={"author": [Person("Author")]},
            fields={
                "title": "Title",
                "journal": "Journal",
                "year": "Year",
                "volume": "Volume",
                "number": "Number",
                "pages": "Pages",
            },
        )

        # no entries in the beginning
        self.assertTupleEqual(self.app.get_entries(), (None, "No entries found"))

        self.app.add_entry(entry)

        # entries can be retrieved when there's an added entry
        self.assertTupleEqual(
            self.app.get_entries(),
            (self.app._bib_data.entries, "Successfully retrieved entries"),
        )

    def test_delete_all_entries_works(self):
        # populating 1 entry via an earlier test
        self.test_add_entry()

        self.app.del_entries([])

        # entries should be empty
        self.assertTupleEqual(self.app.get_entries(), (None, "No entries found"))

    def test_delete_specific_entries_works(self):
        # populating 1 entry via an earlier test
        self.test_add_entry()

        # adding +1 entry so we have more than one
        entry = Entry(
            "article",
            fields={
                "author": "Author2",
                "title": "Title2",
                "journal": "Journal2",
                "year": "Year2",
                "volume": "Volume2",
                "number": "Number2",
                "pages": "Pages2",
            },
        )
        self.app.add_entry(entry)

        # adding a 3rd entry
        entry = Entry(
            "article",
            fields={
                "author": "Author3",
                "title": "Title3",
                "journal": "Journal3",
                "year": "Year3",
                "volume": "Volume3",
                "number": "Number3",
                "pages": "Pages3",
            },
        )
        self.app.add_entry(entry)

        # storing keys of entries here
        entries, _msg = self.app.get_entries()

        # deleting 1st and 2nd entry
        self.app.del_entries([0, 1])

        # should have 1 entry left
        entries, _msg = self.app.get_entries()
        self.assertEqual(len(entries), 1)

        # deleting 3rd entry
        self.app.del_entries([0])

        # entries should be empty
        self.assertTupleEqual(self.app.get_entries(), (None, "No entries found"))

    def test_search_entries(self):
        for entry in self.entries:
            self.app.add_entry(entry)

        # Save keys for later use as they are uuid4
        keys = list(self.app._bib_data.entries.keys())

        # search for "Title1"
        filtered_entries = self.app.find_entries_by_title("Title1")
        self.assertEqual(len(filtered_entries), 1)
        self.assertEqual(
            filtered_entries[keys[0]].persons["author"][0].last_names[0], "Author1"
        )

        # search for "Title2"
        filtered_entries = self.app.find_entries_by_title("Title2")
        self.assertEqual(len(filtered_entries), 1)
        self.assertEqual(
            filtered_entries[keys[1]].persons["author"][0].last_names[0], "Author2"
        )

        # search for "title"
        filtered_entries = self.app.find_entries_by_title("title")
        self.assertEqual(len(filtered_entries), 3)

    def test_valid_doi_returns_bibtex(self):
        # This is a valid DOI
        doi = "10.1145/2783446.2783605"
        bibtex = self.app.get_bibtex_by_doi(doi)

        # bibtex should start with " @"
        self.assertTrue(bibtex.startswith(" @"))

    def test_doi_not_found_returns_infomessage(self):
        # This is an invalid DOI
        doi = "10.1145/2783446.2783605x"
        bibtex = self.app.get_bibtex_by_doi(doi)
        self.assertEqual(bibtex, "DOI not found.")

    @patch("urllib.request.urlopen")
    def test_doi_service_not_available_returns_infomessage(self, mock_urlopen):
        # Make urlopen mock raise an HTTPError
        mock_urlopen.side_effect = HTTPError(
            "http://notworkingurl.com/", 503, "Service unavailable", {}, None
        )

        # This is a valid DOI
        doi = "10.1145/2783446.2783605"
        bibtex = self.app.get_bibtex_by_doi(doi)

        # Mocked urlopen should raise an HTTPError with 503 status code
        self.assertEqual(bibtex, "Service unavailable.")
