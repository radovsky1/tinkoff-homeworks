import os

from collections.abc import MutableMapping
from contextlib import suppress


class FileDict(MutableMapping):
    def __init__(self, dirname, pairs=None, **kwargs):
        if pairs is None:
            pairs = {}
        self.dirname = dirname
        with suppress(FileExistsError):
            os.mkdir(dirname)
        self.update(pairs, **kwargs)

    def __getitem__(self, key):
        fullpath = os.path.join(self.dirname, key)
        try:
            with open(fullpath, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise KeyError(key) from None

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, value):
        fullpath = os.path.join(self.dirname, key)
        with open(fullpath, "w") as f:
            f.write(value)

    def __delitem__(self, key):
        fullpath = os.path.join(self.dirname, key)
        try:
            os.remove(fullpath)
        except FileNotFoundError:
            raise KeyError(key) from None

    def __iter__(self):
        return iter(os.listdir(self.dirname))

    def __len__(self):
        return len(os.listdir(self.dirname))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dirname!r})"
