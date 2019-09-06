from .rpg_object import Thing, Exit, Direction, Place as PlaceModel


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
            raise ServerMessage.CannotParse(j, e)

    @staticmethod
    def _parse_json(j):
        method = '_parse_by_tag' if 'tag' in j else '_parse_by_type'
        return getattr(ServerMessage, method)(j)

    @staticmethod
    def _parse_by_tag(j):
        tag = j['tag']
        if tag == 'SendCredentials':
            cls = SendCredentials
        elif tag == 'Welcome':
            cls = Welcome
        else:
            raise KeyError(f"tag '{tag}' not recognized")
        return cls.from_json(j.get('contents'))

    @staticmethod
    def _parse_by_type(j):
        typ = j['type']
        if typ == 'joined':
            cls = Joined
        elif typ == 'youare':
            cls = YouAre
        elif typ == 'thingdescription':
            cls = ThingDescription
        elif typ == 'thingedited':
            cls = ThingEdited
        elif typ == 'looked':
            cls = Looked
        elif typ == 'place':
            cls = Place
        elif typ == 'exits':
            cls = Exits
        elif typ == 'placecontents':
            cls = PlaceContents
        elif typ == 'said':
            cls = Said
        elif typ == 'whispered':
            cls = Whispered
        elif typ == 'entered':
            cls = Entered
        elif typ == 'exited':
            cls = Exited
        else:
            raise KeyError(f"type '{typ}' not recognized")
        return cls.from_json(j['value'])


class SendCredentials(ServerMessage):

    @staticmethod
    def from_json(_):  # arg should be None
        return SendCredentials()


class Welcome(ServerMessage):
    def __init__(self, idn):
        self.id = idn

    @staticmethod
    def from_json(j):
        return Welcome(j)


class YouAre(ServerMessage):

    def __init__(self, thing):
        """
        Args:
            thing (json): should be a full Thing, including description
        """
        self.thing = thing

    @staticmethod
    def from_json(j):
        thing = Thing.from_json(j)
        return YouAre(thing)


class ThingDescription(ServerMessage):
    """
    The description of some Thing
    """
    def __init__(self, thing_id, description):
        """
        Args:
            thing_id (int):
            description (str):
        """
        self.thing_id = thing_id
        self.description = description

    @staticmethod
    def from_json(j):
        return ThingDescription(j['tid'], j['dsc'])


class ThingEdited(ServerMessage):
    """
    A Thing has been edited (so you may want to request its description).
    """
    def __init__(self, thing_id):
        """
        Args:
            thing_id (int):
        """
        self.thing_id = thing_id

    @staticmethod
    def from_json(j):
        return ThingEdited(j)


class Looked(ServerMessage):
    """
    A character has looked at some thing or other character.
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
        return Looked(j['looker'], j['lookee'])


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


class Exits(ServerMessage):
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
        return Exits([Exit.from_json(e) for e in j])


class PlaceContents(ServerMessage):
    """
    Information about what things, including characters, are
    in the current place.
    """
    def __init__(self, things):
        """
        Args:
            things (list of Thing): names and IDs only.
        """
        self.things = things

    @staticmethod
    def from_json(j):
        return PlaceContents([Thing.from_json(e) for e in j])


class Said(ServerMessage):
    """
    A character in the current place said something.
    """
    def __init__(self, thing_id, speech):
        self.things = thing_id
        self.speech = speech

    @staticmethod
    def from_json(j):
        return Said(j['speaker'], j['speech'])


class Whispered(ServerMessage):
    """
    A character in the current place whispered something to a thing or other
    character.
    """
    def __init__(self, from_id, to_id, speech):
        self.from_id = from_id
        self.to_id = to_id
        self.speech = speech

    @staticmethod
    def from_json(j):

        return Whispered(j['from'], j['to'], j['speech'])


class Entered(ServerMessage):
    """
    A character has just entered the current place through one of the exits.
    """
    def __init__(self, exit_name, thing, nbr_name, direction):
        """
        Args:
            exit_name (str):
            thing (Thing): actually contains only the name and id
            nbr_name (str): name of the place from which the character entered
            direction (Direction):
        """
        self.exit_name = exit_name
        self.thing = thing
        self.nbr_name = nbr_name
        self.direction = direction

    @staticmethod
    def from_json(j):
        thing = Thing(j['tid'], j['tname'])
        direction = getattr(Direction, j['dxn'].upper())
        return Entered(j['ename'], thing, j['nbr'], direction)


class Exited(ServerMessage):
    """
    A character has just left the current place through one of the exits.
    """
    def __init__(self, exit_id, thing_id):
        """
        Args:
            exit_id (int):
            thing_id (int):
        """
        self.exit_id = exit_id
        self.thing_id = thing_id

    @staticmethod
    def from_json(j):
        return Exited(j['eid'], j['tid'])


class Joined(ServerMessage):
    """
    A character has joined the game.
    """
    def __init__(self, thing):
        """
        Args:
            thing (Thing): name and ID only
        """
        self.thing = thing

    @staticmethod
    def from_json(j):
        thing = Thing.from_json(j['value'])
        return Joined(thing)


class Disjoined(ServerMessage):
    """
    A character has left the game.
    """
    def __init__(self, thing_id):
        """
        Args:
            thing_id (int):
        """
        self.thing_id = thing_id

    @staticmethod
    def from_json(j):
        return Disjoined(j['tid'])
