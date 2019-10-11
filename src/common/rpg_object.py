from abc import ABC
from enum import Enum


Direction = Enum('Direction',
                 """
                 NORTH EAST SOUTH WEST
                 NORTHEAST NORTHWEST SOUTHEAST SOUTHWEST
                 """)


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


class Thing(RPGObject):
    def __init__(self, idn, name=None, description=None, awake=None):
        super(Thing, self).__init__(idn)
        self.name = name
        self.description = description
        self.awake = awake

    @staticmethod
    def from_json(j):
        f = Thing.from_list if isinstance(j, list) else Thing.from_object
        return f(j)

    @staticmethod
    def from_list(j):
        return Thing(j[0],
                     j[1] if len(j) > 1 else None,
                     j[2] if len(j) > 2 else None)

    @staticmethod
    def from_object(j):
        return Thing(j['thingId'], j.get('thingName'), j.get('thingDesc'))


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
        # ignore element 0 (address ID)
        return None if j is None else (Address(*j))


class Place(RPGObject):
    def __init__(self, pid, name, desc, address):
        """
        Args:
            pid:
            name:
            desc:
            address (Address): can be None
        """
        super(Place, self).__init__(pid)
        self.name = name
        self.desc = desc
        self.address = address

    @staticmethod
    def from_json(j):
        return Place(j['placeID'], j['placeName'], j['placeDesc'],
                     Address.from_json(j.get('address')))


class Exit(RPGObject):
    def __init__(self, eid, name, dxn, nbr, trans=True):
        """
        Args:
            eid (int):
            name (str):
            dxn (Direction):
            nbr (int, str, Address): reduced Place (id, name, and address)
            trans (bool):
        """
        super(Exit, self).__init__(eid)
        self.name = name
        self.dir = dxn
        self.trans = trans
        self.nbr_id = nbr[0]
        self.nbr_name = nbr[1]
        self.nbr_addr = nbr[2] if nbr[2] else None

    @staticmethod
    def from_json(j):
        dxn = getattr(Direction, j['exitDirection'].upper())
        dst = j['exitDestination']
        addr = Address.from_json(dst[2]) if len(dst) > 2 else None
        nbr = (dst[0], dst[1], addr)
        return Exit(j['exitID'], j['exitName'], dxn, nbr)
