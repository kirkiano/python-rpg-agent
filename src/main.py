import sys
import argparse
import datetime
import random
import time
from collections import defaultdict

from connect import Connection
from bots.pubpeer import scrape_pubpeer
from bots.inteng import scrape_inteng
from bots.retraction_watch import scrape_retwatch
from bots.verge import scrape_verge
from bots.ajp import scrape_ajp
from bots.aps import *
from bots.science import scrape_sciencemag


def connect(host, port, user, pw):
    conn = Connection(host, int(port))
    conn.authenticate(user, pw)
    return conn


def wait_for_place(conn):
    while True:
        m = conn.recv_message()
        if m['type'] == 'place':
            return m['value']


def run(conn, ntitles, waitleave, waitdl, download, do_shuffle=True):
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
        if do_shuffle:
            random.shuffle(unseen_pubs)
        for pub in unseen_pubs[:min(ntitles, len(unseen_pubs))]:
            conn.say(pub['title'].strip())
            seen[place['pid']].add(pub['id'])
        time.sleep(waitleave)
        chosen_exit = random.choice([e['eid'] for e in place['exits']])
        conn.take_exit(chosen_exit)


def parse_args():
    parser = argparse.ArgumentParser(description='RPG bot')
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
        help='Name of bot character (without the "bot" suffix)',
        choices=('pubpeer', 'inteng', 'verge', 'retwatch', 'sciencemag',
                 'ajp', 'prd', 'prl', 'prx', 'apsnews', 'apsphysics',
                 'physicstoday')
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
        default=1200,
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
    download = getattr(sys.modules[__name__], 'scrape_' + botname)
    run(conn, ntitles, waitleave, waitdl, download)


if __name__ == '__main__':
    args = parse_args()
    main(args.host, args.port,
         args.botname, args.botpw,
         args.ntitles, args.waitleave, args.waitdl)
