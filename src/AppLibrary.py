""" Library for Robot Framework tests"""
# pylint: skip-file
from app import App
from app_io import StubIO
from main import main
from pybtex.database import Entry, Person


class AppLibrary:
    """Manages the app IO for testing"""

    def __init__(self):
        self._io = StubIO()
        self._app = App()

    def add_input(self, value):
        """Add an input string to the queue"""

        self._io.add_input(value)

    def output_should_contain(self, value: str):
        """Checks the oldest unread output"""
        output = self._io.pop_output()

        if not value in output:
            raise AssertionError(f'"{value}" is not {output}')

    def skip_output(self, n: str = "1"):
        """
        Pop output string from the queue without checking.
        Useful for irrelevant lines.
        """
        for _ in range(int(n)):
            self._io.pop_output()

    def run_application(self):
        """Run the app with predetermined inputs."""
        main(self._io, self._app)

    def add_entry(self, citekey: str, author: str, fields: dict):
        """Manual entry add for testing"""
        entry = Entry(
            "article",
            persons={"author": [Person(name) for name in author.split(" and ")]},
            fields=fields,
        )
        self._app._bib_data.entries[citekey] = entry
