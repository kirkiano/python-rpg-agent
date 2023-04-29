from abc import ABCMeta, abstractmethod


class RPGObject(object):

    __metaclass__ = ABCMeta

    def __init__(self, idn):
        """
        A game element, eg, Thing, Place, Exit, Address.

        Args:
            idn (int): ID, unique within the class (ie, a Thing and a Place
                       can have the same numeric ID, and are distinguished
                       by type).
        """
        self._id = idn

    @abstractmethod
    def __str__(self):
        raise NotImplementedError('__str__ not implemented')

    @property
    def id(self):
        return self._id
