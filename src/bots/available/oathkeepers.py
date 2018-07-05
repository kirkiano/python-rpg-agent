from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_oathkeep():
    html = get_web_page('https://www.oathkeepers.org/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(class_='su-post-title')
    sayings = [dict(id=uuid4(), title=t.contents[0].text) for t in tags]
    return sayings


SCRAPERS = [scrape_oathkeep]
