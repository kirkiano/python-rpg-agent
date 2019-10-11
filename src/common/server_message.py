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
        try:
            cls = globals()[tag]
        except KeyError:
            raise KeyError(f"tag '{tag}' not recognized")
        return cls.from_json(j['contents'])


class EventMessage(ServerMessage):
    @staticmethod
    def from_json(j):
        tag = j['tag']
        if tag == 'Joined':
            cls = Joined
        elif tag == 'ThingEdited':
            cls = ThingEdited
        elif tag == 'Looked':
            cls = Looked
        elif tag == 'Said':
            cls = Said
        elif tag == 'Whispered':
            cls = Whispered
        elif tag == 'Entered':
            cls = Entered
        elif tag == 'Exited':
            cls = Exited
        else:
            raise KeyError(f"tag '{tag}' not recognized")
        return cls.from_json(j.get('contents'))

    @staticmethod
    def _parse_by_type(j):
        typ = j['type']
        raise KeyError(f"type '{typ}' not recognized")
        # return cls.from_json(j['value'])


class ValueMessage(ServerMessage):
    @staticmethod
    def from_json(j):
        tag = j['tag']
        if tag == 'YouAre':
            cls = YouAre
        elif tag == 'ThingDescription':
            cls = ThingDescription
        elif tag == 'Place':
            cls = Place
        elif tag == 'Exits':
            cls = Exits
        elif tag == 'PlaceContents':
            cls = PlaceContents
        else:
            raise KeyError(f"tag '{tag}' not recognized")
        return cls.from_json(j.get('contents'))


class Welcome(ValueMessage):
    def __init__(self, idn):
        self.id = idn

    @staticmethod
    def from_json(j):
        return Welcome(j)


class YouAre(ValueMessage):

    def __init__(self, thing):
        """
        Args:
            thing (json): should be a full Thing, including description
        """
        self.thing = thing

    @staticmethod
    def from_json(j):
        return YouAre(Thing.from_json(j))


class ThingDescription(ValueMessage):
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
        return ThingDescription(*j)


class ThingEdited(EventMessage):
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


class Looked(EventMessage):
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
        return Looked(*j)


class Place(ValueMessage):
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


class Exits(ValueMessage):
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


class PlaceContents(ValueMessage):
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


class Said(EventMessage):
    """
    A character in the current place said something.
    """
    def __init__(self, thing_id, speech):
        self.things = thing_id
        self.speech = speech

    @staticmethod
    def from_json(j):
        return Said(*j)


class Whispered(EventMessage):
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
        return Whispered(*j)


class Entered(EventMessage):
    """
    A character has just entered the current place through one of the exits.
    """
    def __init__(self, thing, exit_name, nbr_name, direction):
        """
        Args:
            thing (Thing): actually contains only the name and id
            exit_name (str):
            nbr_name (str): name of the place from which the character entered
            direction (Direction):
        """
        self.thing = thing
        self.exit_name = exit_name
        self.nbr_name = nbr_name
        self.direction = direction

    @staticmethod
    def from_json(j):
        thing = Thing.from_json(j[1])
        direction = getattr(Direction, j[3].upper())
        return Entered(thing, j[0], j[2], direction)


class Exited(EventMessage):
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
        return Exited(j[0], Thing.from_json([j[1]]))


class Joined(EventMessage):
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
        return Joined(Thing.from_json(j))


class Disjoined(EventMessage):
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
        return Disjoined(j)
