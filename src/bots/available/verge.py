from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_verge():
    html = await get_web_page('https://www.theverge.com/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('h2', {'class': 'c-entry-box--compact__title'})
    return [dict(id=uuid4(), title=tag.contents[0].text) for tag in tags
            if hasattr(tag.contents[0], 'text')]


SCRAPERS = [scrape_verge]
