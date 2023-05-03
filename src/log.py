import logging.config
import os

# import coloredlogs

# Consider the advice given at
# https://betterstack.com/community/guides/logging/python/python-logging-best-practices/


def init_logs():
    # the 'upper' is recommended at
    # https://docs.python.org/3/howto/logging.html#logging-to-a-file
    log_level = {
        'top':     os.environ.get('LOG_LEVEL_TOP',        'INFO').upper(),
        'bot':     os.environ.get('LOG_LEVEL_BOT',        'INFO').upper(),
        'roam':    os.environ.get('LOG_LEVEL_ROAM',       'INFO').upper(),
        'speech':  os.environ.get('LOG_LEVEL_SPEECH',  'WARNING').upper(),
        'tcp':     os.environ.get('LOG_LEVEL_TCP',     'WARNING').upper(),
    }
    print(f'Log levels are {log_level}')

    logging_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s %(message)s - %(filename)s:%(lineno)s',
            },
        },
        'handlers': {
            'standard': {
                'level': 'DEBUG',  # lowest level admits everything
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            }
        },
        'loggers': {
            # '': {
            #     'handlers': ['standard'],
            # },
            'top': {
                'level': log_level['top'],
                'handlers': ['standard'],
            },
            'bot': {
                'level': log_level['bot'],
                'handlers': ['standard'],
            },
            'roam': {
                'level': log_level['roam'],
                'handlers': ['standard'],
            },
            'speech': {
                'level': log_level['speech'],
                'handlers': ['standard'],
            },
            'tcp': {
                'level': log_level['tcp'],
                'handlers': ['standard'],
            },
        },
    }

    logging.config.dictConfig(logging_dict)

    # To change the format of log messages, see
    # https://docs.python.org/3/howto/logging.html#changing-the-format-of-displayed-messages
    # and
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    # coloredlogs.install(
    #     level=log_level,
    #     fmt='%(asctime)s,%(msecs)03d %(levelname)s %(filename)s:%(lineno)s - %(message)s'
    # )
