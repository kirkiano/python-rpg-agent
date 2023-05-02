from .object import RPGObject
from .address import Address


class Place(RPGObject):
    def __init__(self, pid, name, desc, address=None):
        """
        Args:
            pid (int):
            name (str):
            desc (str):
            address (Address or None):
        """
        super().__init__(pid)
        self.name = name
        self._desc = desc
        self.address = address

    @staticmethod
    def from_object(j):
        return Place(j['id'], j['name'], j.get('desc'),
                     Address.from_object(j.get('addr')))

    @property
    def description(self):
        return self._desc

    def __str__(self):
        return (f'{self.address}, ' if self.address else '') + self.name

    def __eq__(self, other):
        return self.name == other.name and \
            self.description == other.description and \
            self.address == other.address
