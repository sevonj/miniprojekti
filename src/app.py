from pybtex.database import BibliographyData


class App:
    def __init__(self):
        print("This is the app")
        self._bib_data = None

    def create_bib(self):
        """Load an empty bibliography"""

        self._bib_data = BibliographyData()
