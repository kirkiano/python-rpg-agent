from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_truthdig():
    html = await get_web_page('https://www.truthdig.com/')
    soup = BeautifulSoup(html, 'html.parser')
    attr = 'archive-home__title'
    tags = soup.find_all(class_=lambda a: a and a.startswith(attr))
    sayings = [tag.contents[1].text for tag in tags]
    return [dict(id=uuid4(), title=s) for s in sayings]


SCRAPERS = [scrape_truthdig]
