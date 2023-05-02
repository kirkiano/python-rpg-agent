import logging
import asyncio

from log import init_logs
from args import parse_args
from get_bots import get_scraping_bot_tasks
from server import TCPServer


logger = logging.getLogger('top')


async def main(server_address, botfile, waitleave):
    server = TCPServer(server_address)
    tasks = await get_scraping_bot_tasks(server, botfile, waitleave, logger)
    logger.info(f'Running {len(tasks)} tasks')
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    init_logs()
    args = parse_args()
    main_task = main(*args)
    asyncio.run(main_task)
