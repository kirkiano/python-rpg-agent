from abc import abstractmethod

from exn import RPGException
from model import Char, Exit, NonverbalExpression, Place as PlaceModel, Thing


class CharMessage(object):

    class CannotParse(RPGException):
        def __init__(self, data, reason):
            """
            Args:
                data (str or JSON):
                reason (str or Exception):
            """
            self.data = data
            self.reason = reason
            rsn = reason if isinstance(reason, str) else str(reason)
            msg = f"Cannot parse '{data}' into a CharMessage: {rsn}"
            super().__init__(msg)

    @staticmethod
    def from_object(j):
        try:
            return CharMessage._parse_dict(j)
        except KeyError as e:
            raise CharMessage.CannotParse(j, e)

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

    @abstractmethod
    def __str__(self):
        raise NotImplementedError('CharMessage.__str__ not implemented')


class Welcome(CharMessage):
    def __init__(self, cid, name, desc, health):
        self.cid = cid
        self.name = name
        self.desc = desc
        self.health = health

    @staticmethod
    def from_object(j):
        return Welcome(j['id'], j['name'], j['desc'], j['health'])

    def __str__(self):
        return (f'Welcome, {self.name}. Your ID is {self.cid}, ' +
                f'your health is {self.health}, ' +
                f'and your description is: {self.desc}')


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

    def __str__(self):
        return f'Your location is: {self.place}'


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
        return WaysOut([Exit.from_object(e) for e in j['exits']])

    def __str__(self):
        return (f'Your ways out are: {" || ".join(map(str, self.exits))}'
                if self.exits else 'You have no ways out')


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

    def __str__(self):
        return f'Char with ID {self.cid} has joined the game'


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

    def __str__(self):
        return f'Char with ID {self.cid} has left the game'


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

    def __str__(self):
        return (f'With you here are: {", ".join(map(str, self.chars))}'
                if self.chars else 'There is no one else here.')


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

    def __str__(self):
        return (f'Things here are: {"".join(map(str, self.things))}'
                if self.things else 'There is nothing here')


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

    def __str__(self):
        return f'Char {self.cid} said, "{self.speech}"'


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

    def __str__(self):
        whisp = f' ("{self.speech}")' if self.speech else ''
        return f'Char {self.by} whispered to char {self.to}{whisp}'


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

    def __str__(self):
        eid = self.exit_id
        return f'{self.name} (char {self.cid}) entered through exit {eid}'


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

    def __str__(self):
        return f'Char {self.cid} left through exit {self.exit_id}'


class Looked(CharMessage):
    """
    A character has looked at another.
    """
    def __init__(self, looker_id, lookee_id):
        """
        Args:
            looker_id (int):
            lookee_id (int):
        """
        self.looker_id = looker_id
        self.lookee_id = lookee_id

    @staticmethod
    def from_object(j):
        return Looked(j['lookerId'], j['lookeeId']['val'])

    def __str__(self):
        return f'Char {self.looker_id} looked at {self.lookee_id}'


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

    def __str__(self):
        return f'Char {self.by} {self.nve.past_tense()} at char {self.to}'


class Health(CharMessage):
    """
    Your health level has changed.
    """
    def __init__(self, value):
        """
        :param float value:
        """
        self.value = value

    @staticmethod
    def from_object(j):
        return Health(j['value'])

    def __str__(self):
        return f'Your health level is now {self.value}'


class Ping(CharMessage):
    def __str__(self):
        return 'Ping'


class GameOver(CharMessage, RPGException):
    """
    The game has ended.
    """
    def __init__(self, reason):
        self.reason = reason

    @staticmethod
    def from_object(j):
        return GameOver(j['reason'])

    def __str__(self):
        rsn = f' ({self.reason})' if self.reason else ''
        return f'Game over{rsn}'
