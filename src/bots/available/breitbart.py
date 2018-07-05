from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_breitbart():
    html = await get_web_page('http://www.breitbart.com/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('article')
    tags.extend(soup.find_all('div', {'id': 'BBTrendNow'}))
    sayings = [dict(id=uuid4(), title=t.text) for t in tags]
    return sayings


SCRAPERS = [scrape_breitbart]
