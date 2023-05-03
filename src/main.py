import logging
import asyncio

from log import init_logs
from args import parse_args
from util import keep_trying
from get_bots import get_scraping_bot_tasks
from server import TCPServer


logger = logging.getLogger('top')


async def main(server_address,
               botfile,
               waitleave,
               wait_between_reconnect_attempts):
    server = TCPServer(server_address)

    async def connect(username, srv=server, log=logger):
        return await keep_trying(server.connect,
                                 wait_between_reconnect_attempts,
                                 f'connect {username} to {srv}',
                                 log)
    tasks = await get_scraping_bot_tasks(connect, botfile, waitleave)
    logger.info(f'Running {len(tasks)} tasks')
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    init_logs()
    args = parse_args()
    main_task = main(*args)
    asyncio.run(main_task)
