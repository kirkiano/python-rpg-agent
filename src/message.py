import logging

from model import Char, Thing, Exit, Place as PlaceModel, NonverbalExpression


class ServerMessage(object):
    class CannotParse(Exception):
        def __init__(self, jsn, reason):
            self.jsn = jsn
            self.reason = reason
            rsn = reason if isinstance(reason, str) else str(reason)
            msg = f'Cannot parse {jsn} into a ServerMessage: {rsn}'
            super(ServerMessage.CannotParse, self).__init__(msg)

    @staticmethod
    def from_json(j):
        try:
            return ServerMessage._parse_json(j)
        except KeyError as e:
            logging.warning(f'Ignoring unparseable JSON {j} ({e}).')

    @staticmethod
    def _parse_json(j):
        method = '_parse_by_tag' if 'tag' in j else '_parse_by_type'
        return getattr(ServerMessage, method)(j)

    @staticmethod
    def _parse_by_tag(j):
        tag = j['tag']
        try:
            cls = globals()[tag]
        except KeyError:
            raise KeyError(f"tag '{tag}' not recognized")
        return cls.from_json(j)


class Welcome(ServerMessage):
    def __init__(self, idn, name, desc, health):
        self.id = idn
        self.name = name
        self.desc = desc
        self.health = health

    @staticmethod
    def from_json(j):
        return Welcome(j['id'], j['name'], j['desc'], j['health'])


class Place(ServerMessage):
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
    def from_json(j):
        return Place(PlaceModel.from_json(j))


class WaysOut(ServerMessage):  # ValueMessage):
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
    def from_json(j):
        return WaysOut([Exit.from_json(e) for e in j['exits']])


class Joined(ServerMessage):
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
    def from_json(j):
        return Joined(j['cid'])


class Disjoined(ServerMessage):
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
    def from_json(j):
        return Disjoined(j['cid'])


class Occupants(ServerMessage):
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
    def from_json(j):
        return Occupants([Char.from_json(c) for c in j['chars']])


class Contents(ServerMessage):
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
    def from_json(j):
        return Contents([Thing.from_json(e) for e in j['things']])


class Said(ServerMessage):
    """
    A character in the current place said something.
    """
    def __init__(self, cid, speech):
        self.cid = cid
        self.speech = speech

    @staticmethod
    def from_json(j):
        return Said(j['cid'], j['speech'])


class Whispered(ServerMessage):
    """
    A character in the current place whispered something to another.
    """
    def __init__(self, by, to, speech):
        self.by = by
        self.to = to
        self.speech = speech

    @staticmethod
    def from_json(j):
        return Whispered(j['by'], j['to'], j['speech'])


class Entered(ServerMessage):
    """
    A character has entered the current place.
    """
    def __init__(self, cid, name, exit_id):
        self.cid = cid
        self.name = name
        self.exit_id = exit_id

    @staticmethod
    def from_json(j):
        char = j['chr']
        return Entered(char['id'], char['name'], j['eid'])


class Exited(ServerMessage):
    """
    A character has left the current place.
    """
    def __init__(self, cid, exit_id):
        self.cid = cid
        self.exit_id = exit_id

    @staticmethod
    def from_json(j):
        return Exited(j['cid'], j['eid'])


class Looked(ServerMessage):
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
    def from_json(j):
        return Looked(j['lookerId'], j['lookeeId']['val'])


class Expressed(ServerMessage):
    """
    A character has looked at another.
    """
    def __init__(self, by, to, nve):
        self.to = to
        self.by = by
        self.nve = nve

    @staticmethod
    def from_json(j):
        return Expressed(j['by'], j['to'],
                         NonverbalExpression.from_string(j['nve']))

# class ThingEdited(EventMessage):
#     """
#     A Thing has been edited (so you may want to request its description).
#     """
#     def __init__(self, thing_id):
#         """
#         Args:
#             thing_id (int):
#         """
#         self.thing_id = thing_id
#
#     @staticmethod
#     def from_json(j):
#         return ThingEdited(j)
