import argparse

from server import TCPServer


def parse_args():
    botfile_help = (
        'Text file in which each line specifies the name of a desired bot,'
        ' its password, and the RPG address to which it'
        ' should be confined, all separated by a single space. Any'
        ' whitespace within the address name should be limited to one'
        ' space between its words. No quote marks should be used'
        ' for delimiting.'
    )
    parser = argparse.ArgumentParser(
        description='RPG bots that scrape online periodicals',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--host',
        metavar='HOST',
        default='localhost',
        help='Hostname of server (ie, auth driver)'
    )
    parser.add_argument(
        'port',
        metavar='PORT',
        type=int,
        help='Port on server (ie, auth driver)'
    )
    parser.add_argument(
        'botfile',
        metavar='BOTFILE',
        default='botfile',
        help=botfile_help
    )
    parser.add_argument(
        '--waitleave',
        metavar='WAITLEAVE',
        type=int,
        default=120,
        help='Maximum number of seconds a bot should wait before leaving a room'
    )
    parser.add_argument(
        '--waitdl',
        metavar='WAITDL',
        type=int,
        default=120,
        help='Maxmum number of minutes a bot should wait before redownloading its content'
    )
    args = parser.parse_args()
    server_address = TCPServer.Address(args.host, args.port)
    return server_address, args.botfile, args.waitleave
