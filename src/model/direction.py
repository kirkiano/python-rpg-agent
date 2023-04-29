from enum import Enum, unique


@unique
class Direction(Enum):
    UP = 'u'
    DOWN = 'd'
    NORTH = 'n'
    SOUTH = 's'
    EAST = 'e'
    WEST = 'w'
    NORTHEAST = 'ne'
    NORTHWEST = 'nw'
    SOUTHEAST = 'se'
    SOUTHWEST = 'sw'

    def __str__(self):
        return self.value.upper()


def dxn2code(dxn):
    """
    Convert a Direction to a string code (the inverse of code2dxn)
    Args:
        dxn (:class:Direction):
    Returns:
        str: the code corresponding to `dxn`
    """
    return dxn.value


def code2dxn(code):
    """
    Convert a string code to a Direction (the inverse of dxn2code)
    Args:
        code (str): one of u, d, n, s, e, w, ne, nw, se, sw
    Returns: :class:Direction
    Raises:
        ValueError if `code` is invalid
    """
    return Direction(code)
