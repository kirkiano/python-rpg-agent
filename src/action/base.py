

class Action(object):
    """
    Class representing a bot's action
    """

    async def __call__(self, _bot):
        """
        The action itself, which takes the bot as argument, so as to
        gain access to the bot's state, if needed.

        This default implementation is a noop.
        """
        pass
