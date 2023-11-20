"""
app.py

This module contains the service which the UI code can call.
It should be kept UI-independent; No UI code here.

"""
from pybtex.database import BibliographyData


class App:
    """main app"""

    def __init__(self):
        print("This is the app")
        self._bib_data = None

    def create_bib(self):
        """Load an empty bibliography"""
        print("initializing")
        self._bib_data = BibliographyData()
