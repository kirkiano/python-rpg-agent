from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_newrep():
    html = await get_web_page('https://newrepublic.com/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(class_='card-title')
    sayings = []
    for tag in tags:
        c = tag.contents
        title = c[0].text if hasattr(c[0], 'text') else ''
        subtitle = c[1].text if len(c) > 1 and hasattr(c[1], 'text') else ''
        full = title + (': ' + subtitle if subtitle else '')
        sayings.append(dict(id=uuid4(), title=full))
    return sayings


SCRAPERS = [scrape_newrep]
