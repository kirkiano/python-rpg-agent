import logging
import asyncio

from log import init_logs
from args import parse_args
from util import keep_trying
from bot.get_bots import get_scraping_bot_tasks
from server import TCPServer


logger = logging.getLogger('top')
logger.propagate = False


async def main(server_address, botfile, waitleave, wait_reconnect):
    """
    See args.py re parameters.
    """
    server = TCPServer(server_address)

    async def connect(username, srv=server, log=logger):
        return await keep_trying(server.connect,
                                 wait_reconnect,
                                 f'connect {username} to {srv}',
                                 log)

    pairs = await get_scraping_bot_tasks(connect, botfile, waitleave)
    task_pairs = [(asyncio.create_task(bot.run_safely()), pong_task) for
                  (bot, pong_task) in pairs]
    logger.info(f'Running {len(task_pairs)} pairs of tasks')
    tasks = [task for task_pair in task_pairs for task in task_pair]
    await asyncio.gather(*tasks)  # 'return' not needed


def print_settings(server_address, botfile, waitleave, wait_reconnect):
    logger.info(f'Server address is {server_address}')
    logger.info(f'Botfile is {botfile}')
    logger.info(f'Will wait {wait_reconnect} seconds '
                'before trying to connect again to server')
    logger.info(f'Bots will wait at most {waitleave} seconds before moving')


if __name__ == '__main__':
    init_logs()
    args = parse_args()
    print_settings(*args)
    main_task = main(*args)
    asyncio.run(main_task)
