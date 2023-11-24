"""App IO"""


class AppIO:
    """Injected IO handler"""

    def __init__(self) -> None:
        pass

    def print(self, *args) -> None:
        """print wrapper"""
        print(*args)

    def input(self, *args) -> str:
        """input wrapper"""
        return input(*args)


class StubIO:
    """Fake IO handler for testing"""

    def __init__(self) -> None:
        self._outputs = []
        self._inputs = []

    def print(self, *args) -> None:
        """Fake print for the app"""

        # Turn args into string and store them
        output_text = " ".join(map(str, args))
        self._outputs.append(output_text)

    def input(self, *_args) -> str | None:
        """Fake input for the app"""

        # Turn args into string and store them
        # Probably better without
        # output_text = " ".join(map(str, args))
        # self._outputs.append(output_text)

        if len(self._inputs) == 0:
            return None

        return self._inputs.pop(0)

    def add_input(self, text: str) -> None:
        """This allows test script to add inputs to the queue"""

        self._inputs.append(text)

    def pop_output(self) -> str | None:
        """This allows test script to get outputs from the queue"""

        if len(self._outputs) == 0:
            return None

        return self._outputs.pop(0)
