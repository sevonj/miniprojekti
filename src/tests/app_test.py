"""
app_test.py

This module contains unit tests for the App class.

"""
# pylint: disable=protected-access missing-class-docstring missing-function-docstring

import unittest
import os.path
from unittest.mock import patch
from urllib.error import HTTPError
from pybtex.database import BibliographyData, Entry, Person, InvalidNameString
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

        # Temp dir
        if not os.path.exists(TEMP_FILE_PATH):
            os.makedirs(TEMP_FILE_PATH)

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

    def test_edit_entries_author(self):
        entry = Entry(
            "article",
            fields={
                "author": "Test_Author",
                "title": "Test_Title",
                "journal": "Test_Journal",
                "year": "Test_Year",
                "volume": "Test_Volume",
                "number": "Test_Number",
                "pages": "Test_Pages",
            },
        )

        self.app.add_entry(entry)
        keys = []
        for citekey, entry in self.app.get_entries()[0].items():
            keys.append(citekey)
        citekey = keys[-1]
        new_author_name = "New_Name"
        result = self.app.edit_entry(citekey, "author", new_author_name)

        # Assert that the edit was successful
        self.assertTrue(result)

        # Retrieve the edited entry and verify the changes
        edited_entry = self.app._bib_data.entries[citekey]
        edited_author_name = edited_entry.persons["author"][0].last_names[0]
        self.assertEqual(edited_author_name, new_author_name)

    def test_edit_entries_others(self):
        entry = Entry(
            "article",
            fields={
                "author": "Test_Author",
                "title": "Test_Title",
                "journal": "Test_Journal",
                "year": "Test_Year",
                "volume": "Test_Volume",
                "number": "Test_Number",
                "pages": "Test_Pages",
            },
        )

        self.app.add_entry(entry)
        keys = []
        for citekey, entry in self.app.get_entries()[0].items():
            keys.append(citekey)
        citekey = keys[-1]
        new_author_name = "New_Title"
        result = self.app.edit_entry(citekey, "title", new_author_name)

        # Assert that the edit was successful
        self.assertTrue(result)

        # Retrieve the edited entry and verify the changes
        edited_entry = self.app._bib_data.entries[citekey]
        edited_title_name = edited_entry.fields["title"]
        self.assertEqual(edited_title_name, new_author_name)
    
    def test_edit_entries_others_wrong(self):
        entry = Entry(
            "article",
            fields={
                "author": "Test_Author",
                "title": "Test_Title",
                "journal": "Test_Journal",
                "year": "Test_Year",
                "volume": "Test_Volume",
                "number": "Test_Number",
                "pages": "Test_Pages",
            },
        )

        self.app.add_entry(entry)
        keys = []
        for citekey, entry in self.app.get_entries()[0].items():
            keys.append(citekey)
        citekey = keys[-1]
        # Trying to edit a field that shouldn't be changed
        new_issn = "1340-0218"
        result = self.app.edit_entry(citekey, "issn", new_issn)

        # Assert that the edit was unsuccessful
        self.assertFalse(result)


    def test_valid_doi_returns_bibtex(self):
        # This is a valid DOI
        doi = "10.1145/2783446.2783605"
        success, bibtex = self.app.get_bibtex_by_doi(doi)

        # valid doi returns tuple starting with True
        self.assertTrue(success)

        # valid doi returns tuple where bibtex should start with " @"
        self.assertTrue(bibtex.startswith(" @"))

    def test_doi_not_found_returns_infomessage(self):
        # This is an invalid DOI
        doi = "10.1145/2783446.2783605x"
        success, bibtex = self.app.get_bibtex_by_doi(doi)

        # invalid doi returns tuple starting with False
        self.assertFalse(success)

        # invalid doi returns tuple where bibtex should be an infomessage
        self.assertEqual(bibtex, "\n\tDOI not found.\n")

    @patch("urllib.request.urlopen")
    def test_doi_service_not_available_returns_infomessage(self, mock_urlopen):
        # Make urlopen mock raise an HTTPError
        mock_urlopen.side_effect = HTTPError(
            "http://notworkingurl.com/", 503, "Service unavailable", {}, None
        )

        # This is a valid DOI
        doi = "10.1145/2783446.2783605"
        success, bibtex = self.app.get_bibtex_by_doi(doi)

        # unsuccessful search returns tuple starting with False
        self.assertFalse(success)

        # Mocked urlopen should raise an HTTPError with 503 status code
        self.assertEqual(bibtex, "\n\tService unavailable.\n")

    def test_parse_entry_from_bibtex(self):
        # This is a valid BibTeX entry string
        bibtex_entry = """@article{key,
                            author={Maksimainen, Ville},
                            title={Article of Testing},
                            year={1980},
                            journal={Journal of Test Articles},
                            volume={1},
                            pages={10}}"""
        success, entry = self.app.parse_entry_from_bibtex(bibtex_entry)

        # parsed entry should be an instance of Entry
        self.assertIsInstance(entry, Entry)

        # parsed entry should be a success
        self.assertTrue(success)

        # parsed entry should have correct fields
        self.assertEqual(entry.fields["title"], "Article of Testing")
        self.assertEqual(entry.fields["year"], "1980")
        self.assertEqual(entry.fields["journal"], "Journal of Test Articles")
        self.assertEqual(entry.fields["volume"], "1")
        self.assertEqual(entry.fields["pages"], "10")

        # parsed entry should have correct persons
        self.assertEqual(entry.persons["author"][0].last_names[0], "Maksimainen")
        self.assertEqual(entry.persons["author"][0].first_names[0], "Ville")

    def test_parse_entry_from_bibtex_with_invalid_bibtex_returns_none(self):
        # This is an invalid BibTeX entry string
        bibtex_entry = """@article{key,
                            author={Maksimainen, Ville, Viinanen, Kimmo},
                            title={Article of Testing},
                            year={1980},
                            journal={Journal of Test Articles},
                            volume={1},
                            pages={10}"""
        success = self.app.parse_entry_from_bibtex(bibtex_entry)[0]

        # unsuccessful parsing raises an exception
        self.assertRaises(InvalidNameString)

        # unsuccessful parsing returns tuple starting with False
        self.assertFalse(success)
