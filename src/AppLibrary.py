""" Library for Robot Framework tests"""
# pylint: disable=invalid-name
from app_io import StubIO
from main import main


class AppLibrary:
    """Manages the app IO for testing"""

    def __init__(self):
        self._io = StubIO()

    def add_input(self, value):
        """Add an input string to the queue"""

        self._io.add_input(value)

    def output_should_contain(self, value: str):
        """Checks the oldest unread output"""
        output = self._io.pop_output()

        if not value in output:
            raise AssertionError(f'"{value}" is not {output}')
    
    def output_should_not_contain(self, value: str):
        """Checks the oldest unread output"""
        output = self._io.pop_output()

        if value == output:
            raise AssertionError(f'"{value}" is {output}')

    def skip_output(self):
        """
        Pop output string from the queue without checking.
        Useful for irrelevant lines.
        """
        self._io.pop_output()

    def run_application(self):
        """Run the app with predetermined inputs."""
        main(self._io)
