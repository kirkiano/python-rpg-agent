from .object import RPGObject
from .direction import code2dxn
from .place import Place


class Exit(RPGObject):
    def __init__(self, eid, dxn, port, nbr):
        """
        Args:
            eid (int):
            dxn (Direction):
            port (str): the (conceptual) portal
            nbr (Place): the neighboring place, to which this exit leads
        """
        super().__init__(eid)
        self._dir = dxn
        self._nbr = nbr
        self._port = port

    @staticmethod
    def from_object(j):
        dxn = code2dxn(j['dir'])
        nbr = Place.from_object(j['nbr'])
        return Exit(j['id'], dxn, j['port'], nbr)

    @property
    def neighbor(self):
        return self._nbr

    @property
    def portal(self):
        return self._port

    @property
    def direction(self):
        return self._dir

    def __str__(self):
        return (f'exit {self.id}, {self.direction} through {self.portal} ' +
                f'to {self.neighbor}')
