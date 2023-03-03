from abc import ABC
from typing import Iterable


class NewBaseRepository(ABC):
    def __init__(self):
        self._data = None

    def add(self, batch):
        pass

    def add_all(self, batch: Iterable):
        pass

    def get_all(self) -> Iterable:
        pass


class MemoryMockRepository(NewBaseRepository):
    def __init__(self):
        super().__init__()
        self._data = list()

    def add(self, batch):
        self._data.append(batch)

    def add_all(self, batch):
        for itm in batch:
            self._data.append(itm)

    def get_all(self):
        return self._data

    def _delete_all(self):
        self._data = set()

    def __str__(self):
        s = "\n".join(f'{i} - {itm}' for i, itm in enumerate(self._data))
        return f"{type(self).__name__} > Data: '''\n{s}'''\n"
