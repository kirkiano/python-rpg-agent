from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_wolfstreet():
    html = await get_web_page('https://wolfstreet.com/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('h1', {'class': 'entry-title'})
    return [dict(id=uuid4(), title=t.contents[1].text) for t in tags
            if hasattr(t.contents[1], 'text')]


SCRAPERS = [scrape_wolfstreet]
