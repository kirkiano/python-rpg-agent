
import asyncio

from log import init_logs
from args import parse_args
from scrape import get_scraping_bots
from server import TCPServer


async def main(server_address, botfile, bot_params):
    server = TCPServer(server_address)
    bots = await get_scraping_bots(server, botfile, bot_params)
    tasks = [asyncio.create_task(bot.run_safely()) for bot in bots]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    init_logs()
    args = parse_args()
    main_task = main(*args)
    asyncio.run(main_task)
