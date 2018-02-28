import argparse
import datetime
import random
import time
from collections import defaultdict

from bots.pubpeer import download_latest_from_pubpeer
from bots.inteng import download_interesting_engineering
from connect import Connection


def connect(host, port, user, pw):
    conn = Connection(host, int(port))
    conn.authenticate(user, pw)
    return conn


def wait_for_place(conn):
    while True:
        m = conn.recv_message()
        if m['type'] == 'place':
            return m['value']


def run(conn, ntitles, waitleave, waitdl, download):
    conn.recv_message()  # welcome
    conn.look()
    t0 = datetime.datetime.now() - datetime.timedelta(minutes=1 + waitdl)
    pubs = []
    seen = defaultdict(set)
    while True:
        place = wait_for_place(conn)
        t1 = datetime.datetime.now()
        if t1 - t0 > datetime.timedelta(minutes=waitdl):
            t0 = t1
            pubs = download()
        unseen_pubs = [p for p in pubs if p['id'] not in seen[place['pid']]]
        for pub in unseen_pubs[:min(ntitles, len(unseen_pubs))]:
            conn.say(pub['title'].strip())
            seen[place['pid']].add(pub['id'])
        time.sleep(waitleave)
        chosen_exit = random.choice([e['prtid'] for e in place['exits']])
        conn.take_exit(chosen_exit)


def parse_args():
    parser = argparse.ArgumentParser(description='RPG bot for PubPeer')
    parser.add_argument(
        '--host',
        metavar='HOST',
        default='localhost',
        help='server hostname'
    )
    parser.add_argument(
        'port',
        metavar='PORT',
        type=int,
        help='server port'
    )
    parser.add_argument(
        'botname',
        metavar='BOTNAME',
        help='Name of bot character',
        choices=('pubpeerbot', 'intengbot')
    )
    parser.add_argument(
        'botpw',
        metavar='BOTPW',
        help='Password of bot character'
    )
    parser.add_argument(
        '--ntitles',
        metavar='NTITLES',
        type=int,
        default=1,
        help='Number of PubBeer titles to announce'
    )
    parser.add_argument(
        '--waitleave',
        metavar='WAITLEAVE',
        type=int,
        default=600,
        help='Time (seconds) bot waits before leaving a room'
    )
    parser.add_argument(
        '--waitdl',
        metavar='WAITDL',
        type=int,
        default=1200,
        help='Time (minutes) bot waits before redownloading'
    )
    return parser.parse_args()


def main(host, port, botname, botpw, ntitles, waitleave, waitdl):
    conn = connect(host, port, botname, botpw)
    if botname == 'pubpeerbot':
        download = download_latest_from_pubpeer
    else:
        download = download_interesting_engineering
    run(conn, ntitles, waitleave, waitdl, download)


if __name__ == '__main__':
    args = parse_args()
    main(args.host, args.port,
         args.botname, args.botpw,
         args.ntitles, args.waitleave, args.waitdl)
