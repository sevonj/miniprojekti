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
