import argparse


def parse_args():
    botfile_help = (
        'Text file in which each line has the name of a desired bot,'
        ' its password, and the RPG address to which it'
        ' should be confined, all separated by a single space. Any'
        ' whitespace inside the address name should be limited to one'
        ' space between its words, and no quote marks should be used'
        ' to delimit it.'
    )
    parser = argparse.ArgumentParser(
        description='RPG bots that scrape online periodicals',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--host',
        metavar='HOST',
        default='localhost',
        help='Hostname of server (live driver)'
    )
    parser.add_argument(
        'port',
        metavar='PORT',
        type=int,
        help='Port on server (live driver)'
    )
    parser.add_argument(
        'botfile',
        metavar='BOTFILE',
        help=botfile_help
    )
    parser.add_argument(
        '--ntitles',
        metavar='NTITLES',
        type=int,
        default=1,
        help='Max number of titles a bot announces per visit to a room'
    )
    parser.add_argument(
        '--waitleave',
        metavar='WAITLEAVE',
        type=int,
        default=1200,
        help='Maximum time (seconds) bot waits before leaving a room'
    )
    parser.add_argument(
        '--waitdl',
        metavar='WAITDL',
        type=int,
        default=1200,
        help='Maxmum time (minutes) bot waits before redownloading'
    )
    return parser.parse_args()
