
import asyncio
import logging

from log import init_logs
from args import parse_args
from scrape import get_scraping_bot_tasks
from server import TCPServer


async def main(server_address, botfile, bot_params):
    server = TCPServer(server_address)
    task_pairs = await get_scraping_bot_tasks(server, botfile, bot_params)
    tasks = [task for pair in task_pairs for task in pair]
    logging.info(f'Running {len(tasks)} tasks')
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    init_logs()
    args = parse_args()
    main_task = main(*args)
    asyncio.run(main_task)
