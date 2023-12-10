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

    def skip_output(self, n: str = "1"):
        """
        Pop output string from the queue without checking.
        Useful for irrelevant lines.
        """
        for _ in range(int(n)):
            self._io.pop_output()

    def run_application(self):
        """Run the app with predetermined inputs."""
        main(self._io)
