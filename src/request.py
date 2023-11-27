from abc import ABCMeta, abstractmethod


class Login(object):
    """A convenience for authenticating."""

    def __init__(self, username, password):
        """
        :param str username:
        :param str password:
        """
        self.username = username
        self.password = password

    def __str__(self):
        return f'Login as {self.username}'

    def to_dict(self):
        namepass = {
            'name': self.username,
            'pass': self.password
        }
        return {'NamePassword': namepass}


###########################################################
# char requests

class CharRequest(object):
    """Abstract base class of character requests"""
    __metaclass__ = ABCMeta

    def __str__(self):
        return f'{self.__dict__}'

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError('CharRequest.__eq__ not implemented')

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError('CharRequest.to_dict not implemented')


class TakeExit(CharRequest):
    """Request to move to an adjecent place"""
    def __init__(self, exit_id):
        """
        :param int exit_id:
        """
        self.exit_id = exit_id

    def __eq__(self, other):
        return self.exit_id == other.exit_id

    def __str__(self):
        return f'TakeExit({self.exit_id})'

    def to_dict(self):
        return dict(tag='Exit', eid=self.exit_id, details=True)


class Say(CharRequest):
    """Request to say something"""
    def __init__(self, speech):
        """
        :param str speech: the speech to say
        """
        self.speech = speech

    def __eq__(self, other):
        return self.speech == other.speech

    def __str__(self):
        return f'Say: "{self.speech}"'

    def to_dict(self):
        return dict(tag='Say', speech=self.speech)


class Pong(CharRequest):
    """Response to a ping from the server"""
    def __eq__(self, other):
        return isinstance(other, Pong)

    def __str__(self):
        return 'Pong'

    def to_dict(self):
        return dict(tag='Pong')
