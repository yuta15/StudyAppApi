from contextlib import contextmanager
from typing import Generator


class DummySession:
    def __init__(self):
        self.is_called = False

    @contextmanager
    def begin(self) -> Generator[None, None, None]:
        self.is_called = True
        yield self
