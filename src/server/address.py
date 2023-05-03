from dataclasses import dataclass


@dataclass
class Address:
    host: str
    port: int

    def __str__(self):
        return f'{self.host}:{self.port}'
