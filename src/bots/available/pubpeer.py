import json
import aiohttp


async def scrape_pubpeer():
    async with aiohttp.request('GET', 'https://pubpeer.com/api/recent') as resp:
        body = await resp.text()
        jsn = json.loads(body)
        tags = [
            dict(id=pub['id'],
                 title=pub['title'],
                 journals=set([jrn['title']
                               for jrn in pub['journals']['data']]))
            for pub in jsn['publications']
        ]
        return tags


SCRAPERS = [scrape_pubpeer]
