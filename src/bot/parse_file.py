

def botfile_to_dict(botfile):
    """
    Parse a botfile into a dictionary. The botfile should specify
    a bot per line and should contain no blank lines. Each line should
    contain, in this order:
      - the bot's username in the RPG
      - the password for that username
      - the name of the address to which the bot should be confined

    These three fields should be separated by whitespace. It is not an
    error for the last field (the address) to contain internal whitespace,
    though each occurrence of that whitespace will be converted to a single
    space.

    Args:
        botfile (str): path to the botfile

    Returns:
        dict: keys are bot names, values are tuples pairing the password
        and the address
    """

    with open(botfile, 'r') as f:
        contents = f.readlines()

    def make_bot_data_tuple(line):
        parts = line.split()
        if len(parts) < 3:
            raise Exception(f'botfile malformed at "{line}"')
        return parts[0], (parts[1], ' '.join(parts[2:]))

    return dict([make_bot_data_tuple(line) for line in contents])
