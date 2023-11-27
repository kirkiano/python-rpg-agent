import asyncio


async def keep_trying(f, wait_secs, desc, logger):
    """
    :param func f: a thunk executing the computation to keep attempting
    :param int wait_secs: number of seconds to wait before retrying
    :param str desc: grammatical predicate describing f (eg, "connect to db")
    :param Logger logger: a logger to log to
    :return: whatever f returns
    """
    """
    Keep trying to invoke f until it succeeds, ie, until it doesn't throw an
    exception.

    Args:
        f (thunk): the computation to keep attempting
        wait_secs (int): number of seconds to wait before retrying
        desc (str): grammatical predicate describing f (eg, "connect to db")
        logger (Logger):

    Returns:
        whatever f returns
    """
    n = 1
    while True:
        try:
            return await f()
        except Exception as e:  # for generality, catch all excpetions
            logger.warning(f'Attempt no. {n} to {desc} has FAILED: {e}.'
                           f' Retrying in {wait_secs} seconds...')
            n += 1
            await asyncio.sleep(wait_secs)
