from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_newcriterion():
    html = await get_web_page('https://www.newcriterion.com')
    soup = BeautifulSoup(html, 'html.parser')
    tags = [dict(id=uuid4(), title=t.text) for t in soup.find_all('article')]
    return tags


SCRAPERS = [scrape_newcriterion]
