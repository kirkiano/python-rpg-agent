import json
import aiohttp


async def scrape_pubpeer():
    async with aiohttp.request('GET', 'https://pubpeer.com/api/recent') as resp:
        body = await resp.text()
        jsn = json.loads(body)
        tags = [
            dict(id=p['id'],
                 title=p['title'],
                 journals=set([j['title'] for j in p['journals']['data']]))
            for p in jsn['publications']
        ]
        return tags
