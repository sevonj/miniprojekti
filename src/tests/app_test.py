"""
app_test.py

This module contains unit tests for the App class.

"""
# pylint: disable=protected-access missing-class-docstring missing-function-docstring

import unittest
import os.path
from pybtex.database import BibliographyData, Entry, Person
from pybtex.utils import OrderedCaseInsensitiveDict
from app import App

TEMP_FILE_PATH = os.path.join("src", "tests", "temp")
TEST_BIBSTRING = """@article{key,
    AUTHOR = "Lastname, Firstname",
    TITLE = "Title of Article",
    YEAR = "1970",
    JOURNAL = "Journal Name",
    VOLUME = "1",
    PAGES = "10"
}
"""
TEST_ENTRY = Entry(
    "article",
    fields={
        "TITLE": "Title of Article",
        "YEAR": "1970",
        "JOURNAL": "Journal Name",
        "VOLUME": "1",
        "PAGES": "10",
    },
    persons=OrderedCaseInsensitiveDict([("AUTHOR", [Person("Lastname, Firstname")])]),
)


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

    def test_set_bib_path(self):
        # Set str
        test_path = "this/is/a/test/path"
        self.app.set_bib_path(test_path)
        self.assertEqual(self.app._bib_path, test_path)

        # Set None
        test_path = None
        self.app.set_bib_path(test_path)
        self.assertEqual(self.app._bib_path, test_path)

    def test_get_bib_path(self):
        # Get str
        test_path = "this/is/a/test/path"
        self.app._bib_path = test_path
        self.assertEqual(self.app.get_bib_path(), test_path)

        # Get None
        self.app._bib_path = test_path
        self.assertEqual(self.app.get_bib_path(), test_path)

    def test_load_from_file(self):
        test_path = os.path.join(TEMP_FILE_PATH, "test_load_from_file.bib")

        # Delete old bibliography file
        if os.path.exists(test_path):
            os.remove(test_path)

        # Create new bibliography file
        with open(test_path, "w") as f:  # pylint: disable=unspecified-encoding
            f.write(TEST_BIBSTRING)

        # Load bibliography
        self.app.load_from_file(test_path)

        # Verify that the file is correctly loaded
        loaded_entry = self.app._bib_data.entries["key"]
        self.assertEqual(loaded_entry, TEST_ENTRY)

    def test_save_to_file(self):
        test_path = os.path.join(TEMP_FILE_PATH, "test_save_to_file.bib")

        # Delete old test file
        if os.path.exists(test_path):
            os.remove(test_path)

        # Prepare bibliography
        self.app._bib_data.entries["key"] = TEST_ENTRY

        # Save bibliography
        self.app.save_to_file(test_path)

        # Verify that the file is correctly saved
        saved_bibstring = ""
        with open(test_path, "r") as f:  # pylint: disable=unspecified-encoding
            saved_bibstring = str(f.read())
        self.assertEqual(saved_bibstring, TEST_BIBSTRING)

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
