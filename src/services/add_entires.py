from pybtex.database import BibliographyData, Entry


# Create a Get_Entries class with hardcoded entry data
class Get_Entries:
    def __init__(self):
        self.entries = BibliographyData()

    def input_entry(self):
        while True:
            print("Enter article citation details:")
            author = input("Author: ")
            title = input("Title: ")
            journal = input("Journal: ")
            year = input("Year: ")
            volume = input("Volume: ")
            number = input("Number: ")
            pages = input("Pages: ")

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
                self.entries.add_entry("article-minimal", entry)
                print("Entry successfully saved to the database.")
                break
                # hello

    def get_all_entries(self):
        """Return all the entries in a list"""
        return self.entries


entries_app = Get_Entries()

entries_app.input_entry()

# Get the entries and print them in BibTeX format
entries = entries_app.get_all_entries()
print(entries)
print(entries.to_string("bibtex"))

"""
Entry successfully saved to the database.
BibliographyData(
  entries=OrderedCaseInsensitiveDict([
    ('article-minimal', Entry('article',
      fields=[
        ('author', 'John Doe'), 
        ('title', 'Testing Pybtex Entries'), 
        ('journal', 'Test Journal'), 
        ('year', '2023'), 
        ('volume', '10'), 
        ('number', '5'), 
        ('pages', '100-120')],
      persons=OrderedCaseInsensitiveDict([])))]),

  preamble=[])
@article{article-minimal,
    author = "John Doe",
    title = "Testing Pybtex Entries",
    journal = "Test Journal",
    year = "2023",
    volume = "10",
    number = "5",
    pages = "100-120"
}
"""
