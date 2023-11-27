from dataclasses import dataclass


@dataclass
class Address:
    """
    Host and port identifying the game server's socket address
    """
    host: str
    port: int

    def __str__(self):
        return f'{self.host}:{self.port}'
