from pybtex.database import BibliographyData, Entry


class App:
    """main app"""
    def __init__(self):
        print("This is the app")
        self._bib_data = None

    def create_bib(self):
        """Load an empty bibliography"""
        print("initializing")
        self._bib_data = BibliographyData()
    
    def add_entries(self):
        ''' Takes user's input fir the article citation '''
        while True:
            print("Enter article citation details:")
            author = input('Author: ')
            title = input('Title: ')
            journal = input('Journal: ')
            year = input('Year: ')
            volume = input('Volume: ')
            number = input('Number: ')
            pages = input('Pages: ')

            if not any([author, title, journal, year, volume, number, pages]):
                print("An entry is missing, try again.")
            else:
                # Create an Entry object representing the article citation
                entry = Entry(
                    "article",
                    fields={
                        "author": author,
                        "title": title,
                        "journal": journal,
                        "year": year,
                        "volume": volume,
                        "number": number,
                        "pages": pages,
                    },
                )

                # Add the entry to the BibliographyData
                self._bib_data.add_entry("article-minimal", entry)
                print("Entry successfully saved to the database.")
                break
    
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
                
