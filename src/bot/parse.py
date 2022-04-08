
class MalformedBotfile(Exception):
    def __init__(self, line):
        self.line = line
        self.message = f'botfile malformed at "{line}"'


def parse_botline(line):
    """
    Parse a bot line. It should contain three whitespace-separated fields:

      1. the bot's username in the RPG
      2. the password for that username
      3. the name of the address to which the bot should be confined

    It is not an error for the address name to contain internal whitespace,
    though each occurrence of that whitespace will be converted to a single
    space.

    Args:
        line (str):

    Returns:
        tuple: (bot name, password, address name)
    """
    parts = line.split()
    if len(parts) < 3:
        raise MalformedBotfile(line)
    return parts[0], parts[1], ' '.join(parts[2:])
