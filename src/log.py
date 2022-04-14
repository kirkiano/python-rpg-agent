
import os

import coloredlogs


def init_logs():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    print(f'Log level is {log_level}')

    # To change the format of log messages, see
    # https://docs.python.org/3/howto/
    #             logging.html#changing-the-format-of-displayed-messages
    # and https://docs.python.org/3/library/logging.html#logrecord-attributes
    coloredlogs.install(
        level=log_level,
        fmt='%(asctime)s,%(msecs)03d %(levelname)s %(message)s'
    )
