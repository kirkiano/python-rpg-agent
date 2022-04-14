
class RPGException(Exception):
    def __init__(self, msg):
        super(RPGException, self).__init__(f'RPG exception: {msg}')


class RPGClientException(RPGException):
    def __init__(self, client_name, msg):
        super(RPGClientException, self).__init__(f'{client_name}: {msg}')
