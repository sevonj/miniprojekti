"""
app_test.py

This module contains unit tests for the App class.

"""
# pylint: disable=protected-access missing-class-docstring missing-function-docstring

import unittest
from pybtex.database import BibliographyData, Entry
from app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.create_bib()

    def test_create_bib(self):
        self.app._bib_data = None
        self.app.create_bib()
        self.assertEqual(self.app._bib_data, BibliographyData())

    def test_add_entry(self):
        entry = Entry(
            "article",
            fields={
                "author": "Author",
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
            fields={
                "author": "Author",
                "title": "Title",
                "journal": "Journal",
                "year": "Year",
                "volume": "Volume",
                "number": "Number",
                "pages": "Pages",
            },
        )

        # no entries in the beginning
        self.assertTupleEqual(
            self.app.get_entries(),
            (None, "No entries found")
        )

        self.app.add_entry(entry)

        # entries can be retrieved when there's an added entry
        self.assertTupleEqual(
            self.app.get_entries(),
            (self.app._bib_data.entries, "Successfully retrieved entries"),
        )

    def test_delete_all_entries_works(self):

        # populating entries via an earlier test
        self.test_add_entry()

        # deleting ALL entries should return None (implicitly)
        self.assertIsNone(self.app.del_entries())

        # entries should be empty
        self.assertTupleEqual(
            self.app.get_entries(),
            (None, "No entries found")
        )

    def test_deleting_non_existing_entry_handles_key_error(self):
        self.assertEqual(
            "\n\tERROR: you're trying to delete a non-existing entry\n",
            self.app.del_entries(["non-existent key"])
        )
