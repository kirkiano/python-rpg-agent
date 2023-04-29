
from enum import Enum, unique
from exn import RPGException


@unique
class NonverbalExpression(Enum):
    Smile = 1
    Scowl = 2

    @staticmethod
    def from_string(s):
        if s.lower() == 'smile':
            return NonverbalExpression.Smile
        elif s.lower() == 'scowl':
            return NonverbalExpression.Scowl
        else:
            raise RPGException(f'Unknown nonverbal expression: {s}')

    def __str__(self):
        return 'smile' if self == NonverbalExpression.Smile else 'scowl'

    def past_tense(self):
        return 'smiled' if self == NonverbalExpression.Smile else 'scowled'
