from .object import RPGObject


class Thing(RPGObject):
    def __init__(self, idn, name, serial_number):
        super().__init__(idn)
        self.name = name
        self.serial_number = serial_number

    @staticmethod
    def from_object(j):
        return Thing(j['id'], j['name'], j['serial'])

    def __str__(self):
        return f'{self.name} {self.serial_number} (Thing {self.id})'
