import logging

from exn import RPGException
from model import Char, Exit, NonverbalExpression, Place as PlaceModel, Thing


class CharMessage(object):
    class CannotParse(RPGException):
        def __init__(self, jsn, reason):
            self.jsn = jsn
            self.reason = reason
            rsn = reason if isinstance(reason, str) else str(reason)
            msg = f'Cannot parse {jsn} into a CharMessage: {rsn}'
            super(CharMessage.CannotParse, self).__init__(msg)

    class NoExits(CannotParse):
        def __init__(self, jsn):
            super(CharMessage.NoExits, self).__init(jsn, "no exits")

    @staticmethod
    def from_object(j):
        try:
            return CharMessage._parse_dict(j)
        except KeyError as e:
            logging.warning(f'Ignoring unparseable dict {j} ({e}).')

    @staticmethod
    def _parse_dict(j):
        method = '_parse_by_tag' if 'tag' in j else '_parse_by_type'
        return getattr(CharMessage, method)(j)

    @staticmethod
    def _parse_by_tag(j):
        tag = j['tag']
        try:
            cls = globals()[tag]
        except KeyError:
            raise KeyError(f"tag '{tag}' not recognized")
        return cls.from_object(j)


class Welcome(CharMessage):
    def __init__(self, cid, name, desc, health):
        self.cid = cid
        self.name = name
        self.desc = desc
        self.health = health

    @staticmethod
    def from_object(j):
        return Welcome(j['id'], j['name'], j['desc'], j['health'])


class Place(CharMessage):
    """
    Information about the place the player is currently in.
    """
    def __init__(self, place):
        """
        Args:
            place (PlaceModel):
        """
        self.place = place

    @staticmethod
    def from_object(j):
        return Place(PlaceModel.from_object(j))


class WaysOut(CharMessage):
    """
    Information about the exits available from the current place.
    """
    def __init__(self, exits):
        """
        Args:
            exits (list of Exit):
        """
        self.exits = exits

    @staticmethod
    def from_object(j):
        exits = j['exits']
        if not exits:
            raise CharMessage.NoExits()
        else:
            return WaysOut([Exit.from_object(e) for e in exits])


class Joined(CharMessage):
    """
    A character has joined the game.
    """
    def __init__(self, cid):
        """
        Args:
            cid (int): character's ID
        """
        self.cid = cid

    @staticmethod
    def from_object(j):
        return Joined(j['cid'])


class Disjoined(CharMessage):
    """
    A character has left the game.
    """
    def __init__(self, cid):
        """
        Args:
            cid (int): character's ID
        """
        self.cid = cid

    @staticmethod
    def from_object(j):
        return Disjoined(j['cid'])


class Occupants(CharMessage):
    """
    Information about what characters are in the current place.
    """
    def __init__(self, chars):
        """
        Args:
            chars (list of Char):
        """
        self.chars = chars

    @staticmethod
    def from_object(j):
        return Occupants([Char.from_object(c) for c in j['chars']])


class Contents(CharMessage):
    """
    Information about what things are in the current place.
    """
    def __init__(self, things):
        """
        Args:
            things (list of Thing):
        """
        self.things = things

    @staticmethod
    def from_object(j):
        return Contents([Thing.from_object(e) for e in j['things']])


class Said(CharMessage):
    """
    A character in the current place said something.
    """
    def __init__(self, cid, speech):
        self.cid = cid
        self.speech = speech

    @staticmethod
    def from_object(j):
        return Said(j['cid'], j['speech'])


class Whispered(CharMessage):
    """
    A character in the current place whispered something to another.
    """
    def __init__(self, by, to, speech):
        self.by = by
        self.to = to
        self.speech = speech

    @staticmethod
    def from_object(j):
        return Whispered(j['by'], j['to'], j['speech'])


class Entered(CharMessage):
    """
    A character has entered the current place.
    """
    def __init__(self, cid, name, exit_id):
        self.cid = cid
        self.name = name
        self.exit_id = exit_id

    @staticmethod
    def from_object(j):
        char = j['chr']
        return Entered(char['id'], char['name'], j['eid'])


class Exited(CharMessage):
    """
    A character has left the current place.
    """
    def __init__(self, cid, exit_id):
        self.cid = cid
        self.exit_id = exit_id

    @staticmethod
    def from_object(j):
        return Exited(j['cid'], j['eid'])


class Looked(CharMessage):
    """
    A character has looked at another.
    """
    def __init__(self, looker_id, looked_id):
        """
        Args:
            looker_id (int):
            looked_id (int):
        """
        self.looker_id = looker_id
        self.looked_id = looked_id

    @staticmethod
    def from_object(j):
        return Looked(j['lookerId'], j['lookeeId']['val'])


class Expressed(CharMessage):
    """
    A character has looked at another.
    """
    def __init__(self, by, to, nve):
        self.to = to
        self.by = by
        self.nve = nve

    @staticmethod
    def from_object(j):
        return Expressed(j['by'], j['to'],
                         NonverbalExpression.from_string(j['nve']))


class Ping(CharMessage):
    pass


class GameOver(CharMessage, RPGException):
    """
    The game has ended.
    """
    def __init__(self, reason):
        self.reason = reason

    @staticmethod
    def from_object(j):
        return GameOver(j['reason'])