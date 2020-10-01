from .rpg_object import Exit, Place as PlaceModel


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
            pass  # ignore quietly # print(ServerMessage.CannotParse(j, e))

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


# class EventMessage(ServerMessage):
#     @staticmethod
#     def from_json(j):
#         tag = j['tag']
#         if tag == 'Joined':
#             cls = Joined
#         elif tag == 'ThingEdited':
#             cls = ThingEdited
#         elif tag == 'Looked':
#             cls = Looked
#         elif tag == 'Said':
#             cls = Said
#         elif tag == 'Whispered':
#             cls = Whispered
#         elif tag == 'Entered':
#             cls = Entered
#         elif tag == 'Exited':
#             cls = Exited
#         else:
#             raise KeyError(f"tag '{tag}' not recognized")
#         return cls.from_json(j)
#
#     @staticmethod
#     def _parse_by_type(j):
#         typ = j['type']
#         raise KeyError(f"type '{typ}' not recognized")
#         # return cls.from_json(j['value'])


# class ValueMessage(ServerMessage):
#     @staticmethod
#     def from_json(j):
#         tag = j['tag']
#         if tag == 'Place':
#             cls = Place
#         elif tag == 'WaysOut':
#             cls = WaysOut
#         else:
#             # raise KeyError(f"tag '{tag}' not recognized")
#             pass
#         return cls.from_json(j)


class Welcome(ServerMessage):  # ValueMessage):
    def __init__(self, idn):
        self.id = idn

    @staticmethod
    def from_json(j):
        return Welcome(j['cid'])


# class ThingDescription(ValueMessage):
#     """
#     The description of some Thing
#     """
#     def __init__(self, thing_id, description):
#         """
#         Args:
#             thing_id (int):
#             description (str):
#         """
#         self.thing_id = thing_id
#         self.description = description
#
#     @staticmethod
#     def from_json(j):
#         return ThingDescription(*j)


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


# class Looked(EventMessage):
#     """
#     A character has looked at some thing or other character.
#     """
#     def __init__(self, looker_id, looked_id):
#         """
#         Args:
#             looker_id (int):
#             looked_id (int):
#         """
#         self.looker_id = looker_id
#         self.looked_id = looked_id
#
#     @staticmethod
#     def from_json(j):
#         return Looked(*j)


class Place(ServerMessage):  # ValueMessage):
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


# class Contents(ValueMessage):
#     """
#     Information about what things are in the current place.
#     """
#     def __init__(self, things):
#         """
#         Args:
#             things (list of Thing):
#         """
#         self.things = things
#
#     @staticmethod
#     def from_json(j):
#         return Contents([Thing.from_json(e) for e in j['things']])


# class Occupants(ValueMessage):
#     """
#     Information about what characters are in the current place.
#     """
#     def __init__(self, chars):
#         """
#         Args:
#             chars (list of Char):
#         """
#         self.chars = chars
#
#     @staticmethod
#     def from_json(j):
#         return Occupants([Char.from_json(e) for e in j['chars']])


# class Said(EventMessage):
#     """
#     A character in the current place said something.
#     """
#     def __init__(self, char_id, speech):
#         self.char_id = char_id
#         self.speech = speech
#
#     @staticmethod
#     def from_json(j):
#         return Said(char_id=j['cid'], speech=j['speech'])


# class Whispered(EventMessage):
#     """
#     A character in the current place whispered something to a thing or other
#     character.
#     """
#     def __init__(self, from_id, to_id, speech):
#         self.from_id = from_id
#         self.to_id = to_id
#         self.speech = speech
#
#     @staticmethod
#     def from_json(j):
#         return Whispered(*j)


# class Motion(EventMessage):
#     """
#     A character has just entered or exited the current place.
#     """
#     def __init__(self, name, char_id, exit_id):
#         """
#         Args:
#             char_id (int): id of character
#             name (str): character who walked in
#             exit_id (int): id of exit through which the character moved
#         """
#         self.name = name
#         self.char_id = char_id
#         self.exit_id = exit_id


# class Entered(Motion):
#     def __init__(self, name, char_id, exit_id):
#         """
#         See Motion's __init__
#         """
#         super(Entered, self).__init__(name, char_id, exit_id)
#
#     @staticmethod
#     def from_json(j):
#         return Entered(j['name'], j['id'], j['eid'])
#
#
# class Exited(Motion):
#     def __init__(self, name, char_id, exit_id):
#         """
#         See Motion's __init__
#         """
#         super(Exited, self).__init__(name, char_id, exit_id)
#
#     @staticmethod
#     def from_json(j):
#         return Exited(j['name'], j['id'], j['eid'])


# class Joined(EventMessage):
#     """
#     A character has joined the game.
#     """
#     def __init__(self, char):
#         """
#         Args:
#             char (Char): name and ID only
#         """
#         self.char = char
#
#     @staticmethod
#     def from_json(j):
#         return Joined(Char.from_json(j, logged_in=True))


# class Disjoined(EventMessage):
#     """
#     A character has left the game.
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
#         return Disjoined(j)
