

class RPGException(Exception):
    """RPG Exception"""
    def __init__(self, msg):
        super().__init__(f'RPG exception: {msg}')
