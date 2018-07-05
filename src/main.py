import os
import argparse
import datetime
import random
from collections import defaultdict
import asyncio
from traceback import print_exc
from importlib import import_module
from functools import partial, reduce

from connect import Connection


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
        help='Maximum number of titles a bot should announce per download'
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
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Print verbose output',
        dest='verbose',
    )
    return parser.parse_args()


async def run(host, port, bot_name, bot_func, ntitles, waitleave, waitdl,
              ioloop, do_shuffle=True, verbose=False):
    conn = await Connection.login(host, port, bot_name, bot_name, ioloop)
    if verbose:
        print(f'{bot_name} has connected to the RPG server.')
    await conn.recv_message()  # welcome
    await conn.look()  # TODO: consider deleting this look
    t0 = datetime.datetime.now() - datetime.timedelta(minutes=1 + waitdl)
    pubs = []
    seen = defaultdict(set)
    while True:
        location = (await conn.wait_for_place()).location
        if verbose:
            print(f'{bot_name} is now in {location.name}.')
        t1 = datetime.datetime.now()
        wait_to_download = random.uniform(0, waitdl)
        if t1 - t0 > datetime.timedelta(minutes=wait_to_download):
            t0 = t1
            pubs = await bot_func()
            if verbose:
                print(f'{bot_name} has downloaded its content.')
        unseen_pubs = [p for p in pubs if p['id'] not in seen[location.id]]
        if do_shuffle:
            random.shuffle(unseen_pubs)
        for pub in unseen_pubs[:min(ntitles, len(unseen_pubs))]:
            saying = pub['title'].strip()
            await conn.say(saying)
            if verbose:
                print(f'{bot_name} has said: {saying}.')
            seen[location.id].add(pub['id'])
        wait_to_move = random.uniform(0, waitleave)
        await asyncio.sleep(wait_to_move)
        chosen_exit = random.choice([e.id for e in location.exits])
        await conn.take_exit(chosen_exit)


async def run_safely(*args, **kwargs):
    try:
        await run(*args, **kwargs)
    except Exception:  # catching all Exceptions is NOT too broad
        print()
        print(f"{kwargs['bot_name']} crashed:")
        print_exc()


def main(host, port, ntitles, waitleave, waitdl, verbose=False):
    enabled_filenames = [f[:-3] for f in os.listdir('bots/enabled')
                         if f.endswith('.py') and f != '__init__.py']
    enabled_bot_modules = [
        import_module(f'bots.enabled.{f}') for f in enabled_filenames
    ]
    scraper_lists = [getattr(m, 'SCRAPERS')
                     for m in enabled_bot_modules if hasattr(m, 'SCRAPERS')]
    scrapers = reduce(lambda acc, ss: acc + ss, scraper_lists)
    bot_names = [scraper.__name__[7:] for scraper in scrapers]
    ioloop = asyncio.get_event_loop()
    runnit = partial(run_safely, host=host, port=port, ntitles=ntitles,
                     waitleave=waitleave, waitdl=waitdl, ioloop=ioloop,
                     verbose=verbose)
    tasks = [ioloop.create_task(runnit(bot_name=bot_name, bot_func=bot))
             for bot_name, bot in zip(bot_names, scrapers)]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()


if __name__ == '__main__':
    clargs = parse_args()
    main(clargs.host, clargs.port, clargs.ntitles,
         clargs.waitleave, clargs.waitdl, clargs.verbose)
