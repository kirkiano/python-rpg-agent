from abc import ABCMeta, abstractmethod

from exn import RPGException


class Login(object):
    """
    A convenience for authenticating. Notes:
        1. Untagged, because not a real request to the engine
        2. The 'details' flag is to be understood implicitly as True.
    """
    def __init__(self, username, password):
        """
        Args:
            username (str)
            password (str)
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
    __metaclass__ = ABCMeta

    class Unrecognized(RPGException):
        def __init__(self, cid, obj):
            msg = f'Char {cid} make unrecognizable request: {obj}'
            super().__init__(msg)

    def __str__(self):
        return f'{self.__dict__}'

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError('CharRequest.__eq__ not implemented')

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError('CharRequest.to_dict not implemented')


class TakeExit(CharRequest):
    def __init__(self, exit_id):
        """
        Args:
            exit_id (int):
        """
        self.exit_id = exit_id

    def __eq__(self, other):
        return self.exit_id == other.exit_id

    def __str__(self):
        return f'TakeExit({self.exit_id})'

    def to_dict(self):
        return dict(tag='Exit', eid=self.exit_id, details=True)


class Say(CharRequest):
    def __init__(self, speech):
        """
        Args:
            speech (str):
        """
        self.speech = speech

    def __eq__(self, other):
        return self.speech == other.speech

    def __str__(self):
        return f'Say: "{self.speech}"'

    def to_dict(self):
        return dict(tag='Say', speech=self.speech)


class Pong(CharRequest):

    def __eq__(self, other):
        return isinstance(other, Pong)

    def __str__(self):
        return 'Pong'

    def to_dict(self):
        return dict(tag='Pong')


###########################################################
# the stuff below is not needed

# class WhoAmI(CharRequest):
#
#     def to_dict(self):
#         return dict(tag='WhoAmI')


# class WhereAmI(CharRequest):
#
#     def to_dict(self):
#         return dict(tag='WhereAmI')


# class WhatIsHere(CharRequest):
#
#     def to_dict(self):
#         return dict(tag='WhatIsHere')


# class HowCanIExit(CharRequest):
#
#     def to_dict(self):
#         return dict(tag='HowCanIExit')


# class EditMe(CharRequest):
#     def __init__(self, new_description):
#         """
#         Args:
#             new_description (int):
#         """
#         self.new_description = new_description
#
#     def to_dict(self):
#         return dict(tag='EditMe', contents=self.new_description)
#
#
# class DescribeThing(CharRequest):
#     def __init__(self, thing_id):
#         """
#         Args:
#             thing_id (int):
#         """
#         self.thing_id = thing_id
#
#     def to_dict(self):
#         return dict(tag='DescribeThing', contents=self.thing_id)
#
#
# class Whisper(CharRequest):
#     def __init__(self, speech, to_id):
#         """
#         Args:
#             speech (str):
#             to_id (int): thing_id of character whispered to
#         """
#         self.speech = speech
#         self.to_id = to_id
#
#     def to_dict(self):
#         return dict(tag='Whisper', contents=[self.speech, self.to_id])
