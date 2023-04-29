from .object import RPGObject


class Address(RPGObject):
    def __init__(self, idn, name, street_number, street_name, city, country):
        """
        Args:
            name (str): the name of the property
            street_number (int):
            street_name (str):
            city (str):
            country (str):
        """
        super(Address, self).__init__(idn)
        self.name = name
        self._number = street_number
        self._street = street_name
        self.city = city
        self.country = country

    @staticmethod
    def from_object(j):
        if j is None:
            return None

        street = j['street']['name'] if 'street' in j else None
        city = j['street']['city']['name'] if 'street' in j else None
        country = j['street']['city']['country']['name']\
            if 'street' in j else None

        return None if j is None else Address(
            idn=j['id'],
            name=j['name'],
            street_number=j.get('num'),
            street_name=street,
            city=city,
            country=country
        )

    @property
    def street_name(self):
        return self._street

    @property
    def street_number(self):
        return self._number

    def __str__(self):
        return (f'{self.name}, {self.street_number} {self.street_name}, ' +
                f'{self.city}, {self.country} (address {self.id})')

    def __eq__(self, other):
        return self.id == other.id and \
            self.name == other.name and \
            self.street_number == other.street_number and \
            self.street_name == other.street_name and \
            self.city == other.city and \
            self.country == other.country
