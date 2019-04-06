
from io import BytesIO, SEEK_SET, SEEK_END
from typing import Any, Optional


class ResponseStream(object):
    """
    Wraps a response stream so you can use it like a file.
    Shamelessly stolen from https://gist.github.com/obskyr/b9d4b4223e7eaf4eedcd9defabb34f13
    """
    def __init__(self, request_iterator: Any):
        self._bytes = BytesIO()
        self._iterator = request_iterator

    def _load_all(self) -> Any:
        self._bytes.seek(0, SEEK_END)
        for chunk in self._iterator:
            self._bytes.write(chunk)

    def _load_until(self, goal_position: int) -> Any:
        current_position = self._bytes.seek(0, SEEK_END)
        while current_position < goal_position:
            try:
                current_position = self._bytes.write(next(self._iterator))
            except StopIteration:
                break

    def tell(self) -> Any:
        return self._bytes.tell()

    def read(self, size: Optional[int] = None) -> Any:
        left_off_at = self._bytes.tell()
        if size is None:
            self._load_all()
        else:
            goal_position = left_off_at + size
            self._load_until(goal_position)

        self._bytes.seek(left_off_at)
        return self._bytes.read(size)

    def seek(self, position: int, whence: Any = SEEK_SET) -> Any:
        if whence == SEEK_END:
            self._load_all()
        else:
            self._bytes.seek(position, whence)
