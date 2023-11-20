"""
app_test.py

This module contains unit tests for the App class.

"""
# pylint: disable=protected-access missing-class-docstring missing-function-docstring

import unittest
from pybtex.database import BibliographyData
from app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.create_bib()

    def test_create_bib(self):
        self.app._bib_data = None
        self.app.create_bib()
        self.assertEqual(self.app._bib_data, BibliographyData())
