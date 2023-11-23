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

        # populating 1 entry via an earlier test
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
        keys = list(key for key in entries)

        # deleting 1st and 2nd entry
        self.assertIsNone(self.app.del_entries(keys[0:2]))

        # should have 1 entry left
        entries, _msg = self.app.get_entries()
        self.assertEqual(len(entries), 1)

        # deleting 3rd entry (which is the only one at this point, but keys are still valid)
        self.assertIsNone(self.app.del_entries(keys[2:]))

        # entries should be empty
        self.assertTupleEqual(
            self.app.get_entries(),
            (None, "No entries found")
        )
