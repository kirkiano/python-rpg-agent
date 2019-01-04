from abc import ABC
from enum import Enum


Direction = Enum('Direction',
                 """
                 NORTH EAST SOUTH WEST
                 NORTHEAST NORTHWEST SOUTHEAST SOUTHWEST
                 """)


class RPGObject(ABC):
    def __init__(self, id):
        self.id = id


class Thing(RPGObject):
    def __init__(self, id, name, description, awake):
        super(Thing, self).__init__(id)
        self.name = name
        self.description = description
        self.awake = awake

    @staticmethod
    def from_json(j):
        return Thing(**j)


class Location(RPGObject):
    def __init__(self, pid, name, desc, exits):
        super(Location, self).__init__(pid)
        self.name = name
        self.desc = desc
        self.exits = exits

    @staticmethod
    def from_json(j):
        exits = [Exit.from_json(e) for e in j['exits']]
        return Location(j['pid'], j['name'], j['desc'], exits)


class Exit(RPGObject):
    def __init__(self, eid, name, dir, trans, nbr):
        super(Exit, self).__init__(eid)
        self.name = name
        self.dir = dir
        self.trans = trans
        self.nbr_id, self.nbr_name = nbr

    @staticmethod
    def from_json(j):
        dir = getattr(Direction, j['dir'].upper())
        return Exit(j['eid'], j['name'], dir, j['trans'], j['nbr'])
