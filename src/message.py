from rpg_object import Thing, Location


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
        typ = j['type']
        if typ == 'auth':
            cls = Auth
        elif typ == 'joined':
            cls = Joined
        elif typ == 'place':
            cls = Place
        else:
            raise KeyError(f"type '{typ}' not recognized")
        return cls.from_json(j['value'])


class Auth(ServerMessage):
    @staticmethod
    def from_json(j):
        tag = j['tag']
        if tag == 'Welcome':
            return Welcome.from_json(j)
        else:
            raise KeyError(f"tag '{tag}' not recognized")


class Welcome(Auth):

    def __init__(self, id):
        self.id = id

    @staticmethod
    def from_json(j):
        return Welcome(j['contents'])


class Joined(ServerMessage):

    def __init__(self, thing):
        self.thing = thing

    @staticmethod
    def from_json(j):
        thing = Thing.from_json(j['value'])
        return Joined(thing)


class Place(ServerMessage):

    def __init__(self, location):
        self.location = location

    @staticmethod
    def from_json(j):
        return Place(Location.from_json(j))
