from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_mises():
    html = await get_web_page('https://mises.org/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(class_='teaser-title')
    return [dict(id=uuid4(), title=t.contents[0].text) for t in tags]


SCRAPERS = [scrape_mises]