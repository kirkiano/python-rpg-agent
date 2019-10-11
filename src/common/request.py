from abc import abstractmethod, ABCMeta


class Request(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_dict(self):
        pass


class WhoAmI(Request):

    def to_dict(self):
        return dict(tag='WhoAmI')


class WhereAmI(Request):

    def to_dict(self):
        return dict(tag='WhereAmI')


class WhatIsHere(Request):

    def to_dict(self):
        return dict(tag='WhatIsHere')


class WaysOut(Request):

    def to_dict(self):
        return dict(tag='WaysOut')


class EditMe(Request):
    def __init__(self, new_description):
        """
        Args:
            new_description (int):
        """
        self.new_description = new_description

    def to_dict(self):
        return dict(tag='EditMe', contents=self.new_description)


class DescribeThing(Request):
    def __init__(self, thing_id):
        """
        Args:
            thing_id (int):
        """
        self.thing_id = thing_id

    def to_dict(self):
        return dict(tag='DescribeThing', contents=self.thing_id)


class TakeExit(Request):
    def __init__(self, exit_id):
        """
        Args:
            exit_id (int):
        """
        self.exit_id = exit_id

    def to_dict(self):
        return dict(tag='Exit', contents=self.exit_id)


class Say(Request):
    def __init__(self, speech):
        """
        Args:
            speech (str):
        """
        self.speech = speech

    def to_dict(self):
        return dict(tag='Say', contents=self.speech)


class Whisper(Request):
    def __init__(self, speech, to_id):
        """
        Args:
            speech (str):
            to_id (int): thing_id of character whispered to
        """
        self.speech = speech
        self.to_id = to_id

    def to_dict(self):
        return dict(tag='Whisper', contents=[self.speech, self.to_id])
