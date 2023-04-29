from .object import RPGObject


class Char(RPGObject):
    def __init__(self, cid, name, logged_in):
        super(Char, self).__init__(cid)
        self.name = name
        self.logged_in = logged_in

    @staticmethod
    def from_object(j, logged_in=None):
        idn = j['id'] if 'id' in j else j['cid']
        logged_in = j['loggedIn'] if 'loggedIn' in j else logged_in
        return Char(idn, j['name'], logged_in)

    def __str__(self):
        return (f'{self.name} (char {self.id}, ' +
                f'logged {"in" if self.logged_in else "out"})')
