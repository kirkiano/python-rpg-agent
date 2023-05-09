from abc import ABCMeta, abstractmethod

from exn import RPGException


class Confine(object):
    """
    Abstract class specifying whether and how something should be confined
    to a certain region of the RPG's world
    """

    __metaclass__ = ABCMeta

    class OutOfBounds(RPGException):
        def __init__(self, place):
            """
            Args:
                place (Place): the place that is out of bounds
            """
            super().__init__(f'out of bounds: {place}')

    @abstractmethod
    def is_within_bounds(self, _place):
        """
        Indicates whether the given place is within bounds.

        Args:
            _place (Place): the place to test
        Returns:
            bool
        """
        raise NotImplementedError('Confine.is_within_bounds is not implemented')

    def assert_within_bounds(self, place):
        """
        Args:
            place (Place): the place to test
        """
        if not self.is_within_bounds(place):
            raise Confine.OutOfBounds(place)

    def is_valid_exit(self, egress):
        """
        Indicates whether the given exit ('egress', so as not to conflict
        with Python's 'exit') leads to a place that is within bounds

        Args:
            egress (Exit): the exit to test
        Returns:
            bool
        """
        return self.is_within_bounds(egress.neighbor)


class NoConfinement(Confine):
    def is_within_bounds(self, _place):
        return True


class ConfineToAddress(Confine):
    """
    Confine to a given address
    """

    def __init__(self, address):
        """
        Args:
            address: If this is an int, then it will be interpreted as the ID
                     of the address to which to confine. Otherwise it is
                     expected to be a string, in which case it will be interpreted
                     as the name of the address to which to confine.
        """
        self.address = address
        self.field = 'id' if isinstance(self.address, int) else 'name'

    def is_within_bounds(self, place):
        return place.address and \
            self.address == getattr(place.address, self.field)
