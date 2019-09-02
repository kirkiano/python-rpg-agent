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
    def __init__(self, idn, name, description, awake):
        super(Thing, self).__init__(idn)
        self.name = name
        self.description = description
        self.awake = awake

    @staticmethod
    def from_json(j):
        tid = j.get('id', j.get('tid'))
        return Thing(tid, j['name'], j.get('desc'), j.get('awake'))


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
        return Address(j['id'], j['name'], j['number'], j['street'],
                       j['city'], j['country'])


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
        addr_j = j.get('addr')
        addr = Address.from_json(addr_j) if addr_j else None
        return Place(j['pid'], j['name'], j['desc'], addr)


class Exit(RPGObject):
    def __init__(self, eid, name, dxn, trans, nbr):
        """
        Args:
            eid (int):
            name (str):
            dxn (Direction):
            trans (bool):
            nbr (int, str, Address): reduced Place (id, name, and address)
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
        dxn = getattr(Direction, j['dir'].upper())
        dst = j['dst']
        addr = Address.from_json(dst[2]) if dst[2] else None
        nbr = (dst[0], dst[1], addr)
        return Exit(j['eid'], j['name'], dxn, j['trans'], nbr)
