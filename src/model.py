from abc import ABC
from enum import Enum, unique


@unique
class Direction(Enum):
    UP = 'u'
    DOWN = 'd'
    NORTH = 'n'
    SOUTH = 's'
    EAST = 'e'
    WEST = 'w'
    NORTHEAST = 'ne'
    NORTHWEST = 'nw'
    SOUTHEAST = 'se'
    SOUTHWEST = 'sw'


def dxn2code(dxn):
    """
    Convert a Direction to a string code (the inverse of code2dxn)
    Args:
        dxn (:class:Direction):
    Returns:
        str: the code corresponding to `dxn`
    """
    return dxn.value


def code2dxn(code):
    """
    Convert a string code to a Direction (the inverse of dxn2code)
    Args:
        code (str): one of u, d, n, s, e, w, ne, nw, se, sw
    Returns: :class:Direction
    Raises:
        ValueError if `code` is invalid
    """
    return Direction(code)
    # TODO: delete the following
    # if code == 'u':
    #     return Direction.UP
    # elif code == 'd':
    #     return Direction.DOWN
    # elif code == 'n':
    #     return Direction.NORTH
    # elif code == 's':
    #     return Direction.SOUTH
    # elif code == 'e':
    #     return Direction.EAST
    # elif code == 'w':
    #     return Direction.WEST
    # elif code == 'ne':
    #     return Direction.NORTHEAST
    # elif code == 'nw':
    #     return Direction.NORTHWEST
    # elif code == 'se':
    #     return Direction.SOUTHEAST
    # elif code == 'sw':
    #     return Direction.SOUTHWEST
    # else:
    #     raise Exception(f'Unknown Direction code: {code}')


class RPGObject(ABC):
    def __init__(self, idn):
        """
        A game element, eg, Thing, Place, Exit, Address.

        Args:
            idn (int): ID, unique within the class (ie, a Thing and a Place
                       can have the same numeric ID, and are distinguished
                       by type).
        """
        self.id = idn


class Char(RPGObject):
    def __init__(self, cid, name, logged_in):
        super(Char, self).__init__(cid)
        self.name = name
        self.logged_in = logged_in

    @staticmethod
    def from_json(j, logged_in=None):
        idn = j['id'] if 'id' in j else j['cid']
        logged_in = j['loggedIn'] if 'loggedIn' in j else logged_in
        return Char(idn, j['name'], logged_in)


class Thing(RPGObject):
    def __init__(self, idn, name, serial_number):
        super(Thing, self).__init__(idn)
        self.name = name
        self.serial_number = serial_number

    @staticmethod
    def from_json(j):
        return Thing(j['id'], j['name'], j['serial'])


class Address(RPGObject):
    def __init__(self, idn, name, street_number, street_name, city, country):
        """
        Args:
            name (str): the name of the property
            street_number (int):
            street_name (str):
            city (str):
            country (str):
        """
        super(Address, self).__init__(idn)
        self.name = name
        self.number = street_number
        self.street = street_name
        self.city = city
        self.country = country

    @staticmethod
    def from_json(j):
        if j is None:
            return None

        street = j['street']['name'] if 'street' in j else None
        city = j['street']['city']['name'] if 'street' in j else None
        country = j['street']['city']['country']['name']\
            if 'street' in j else None

        return None if j is None else Address(
            idn=j['id'],
            name=j['name'],
            street_number=j.get('num'),
            street_name=street,
            city=city,
            country=country
        )


class Place(RPGObject):
    def __init__(self, pid, name, desc, address):
        """
        Args:
            pid:
            name:
            desc (str): can be None
            address (Address): can be None
        """
        super(Place, self).__init__(pid)
        self.name = name
        self.desc = desc
        self.address = address

    @staticmethod
    def from_json(j):
        return Place(j['id'], j['name'], j.get('desc'),
                     Address.from_json(j.get('addr')))

    def __str__(self):
        return self.name + \
               ((', ' + self.address.name) if self.address else '')


class Exit(RPGObject):
    def __init__(self, eid, dxn, port, nbr):
        """
        Args:
            eid (int):
            dxn (Direction):
            port (str): the (conceptual) portal
            nbr (Place): the neighboring place, to which this exit leads
        """
        super(Exit, self).__init__(eid)
        self.dir = dxn
        self.nbr = nbr
        self.port = port

    @staticmethod
    def from_json(j):
        dxn = code2dxn(j['dir'])
        nbr = Place.from_json(j['nbr'])
        return Exit(j['id'], dxn, j['port'], nbr)
