# User can add entries
# Another function can fetch all entries


class Get_Entries:
    ''' The interface where a user input their entry.'''

    def __init__(self):
        self.entries = []

    def add_entry(self):
        """Just a beginner interface, ideally we need to check
        what the user's input is (limit length, strigify etc...) Also later think
        about the way our entry form should be shaped"""

        while True:
            entry = str(input('Add entry: '))
            if len(entry) == 0:
                print('The entry is empty, try again')
            else:
                self.entries.append(entry)  # Append the entry to the entries list
                print("Entry successfully saved to the database.")
                break
    
    def get_all_entires(self):
        ''' spit out all the entries in a list '''
        return(self.entries)

entries_app = Get_Entries()

entries_app.add_entry()
entries_app.add_entry()
entries_app.add_entry()
entries_app.add_entry()

entries = entries_app.get_all_entires()

for entry in entries:
    print(entry)