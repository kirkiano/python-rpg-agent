import sys
import argparse
import datetime
import random
from collections import defaultdict
import asyncio
from traceback import print_exc

"""
TODO: instead of import these statically, import them dynamically with
import_module. Specific example:

    from importlib import import_module
    ajp = import_module('bots.enabled.ajp')  # ajp.scrape_ajp now available
    
Change function names 'scrape_X' to 'scrape' and distiguish them instead by
prefix, e.g., ajp.scrape.
"""

from connect import Connection
from bots.aps import *
from bots.pubpeer import scrape_pubpeer
from bots.inteng import scrape_inteng
from bots.retraction_watch import scrape_retwatch
from bots.verge import scrape_verge
from bots.ajp import scrape_ajp
from bots.science import scrape_sciencemag


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
        '--ntitles',
        metavar='NTITLES',
        type=int,
        default=1,
        help='Number of titles to announce'
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


async def run(host, port, botname, download, ntitles,
              waitleave, waitdl, ioloop, do_shuffle=True):
    conn = await Connection.login(host, port, botname, botname, ioloop)
    await conn.recv_message()  # welcome
    await conn.look()
    t0 = datetime.datetime.now() - datetime.timedelta(minutes=1 + waitdl)
    pubs = []
    seen = defaultdict(set)
    while True:
        location = (await conn.wait_for_place()).location
        t1 = datetime.datetime.now()
        wait_to_download = random.uniform(0, waitdl)
        if t1 - t0 > datetime.timedelta(minutes=wait_to_download):
            t0 = t1
            pubs = await download()
        unseen_pubs = [p for p in pubs if p['id'] not in seen[location.id]]
        if do_shuffle:
            random.shuffle(unseen_pubs)
        for pub in unseen_pubs[:min(ntitles, len(unseen_pubs))]:
            await conn.say(pub['title'].strip())
            seen[location.id].add(pub['id'])
        wait_to_move = random.uniform(0, waitleave)
        await asyncio.sleep(wait_to_move)
        chosen_exit = random.choice([e.id for e in location.exits])
        await conn.take_exit(chosen_exit)


async def run_safely(*args, **kwargs):
    try:
        await run(*args, **kwargs)
    except Exception:
        print()
        print(f"{kwargs['botname']} crashed:")
        print_exc()


def main(host, port, ntitles, waitleave, waitdl):
    bot_names = ('ajp', 'apsnews', 'apsphysics', 'inteng', 'physicstoday',
                 'prd', 'prl', 'prx', 'pubpeer', 'retwatch', 'sciencemag',
                 'verge')
    downloads = [getattr(sys.modules[__name__], 'scrape_' + bot)
                 for bot in bot_names]
    ioloop = asyncio.get_event_loop()
    runnit = partial(run_safely, host=host, port=port, ntitles=ntitles,
                     waitleave=waitleave, waitdl=waitdl, ioloop=ioloop)
    tasks = [ioloop.create_task(runnit(botname=botname, download=dl))
             for botname, dl in zip(bot_names, downloads)]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()


if __name__ == '__main__':
    clargs = parse_args()
    main(clargs.host, clargs.port, clargs.ntitles,
         clargs.waitleave, clargs.waitdl)
