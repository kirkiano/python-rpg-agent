from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_retwatch():
    r = await get_web_page('https://retractionwatch.com/')
    soup = BeautifulSoup(r, 'html.parser')
    tags = soup.find_all(class_='entry-title')
    return [dict(id=uuid4(), title=t.contents[0].text) for t in tags
            if hasattr(t.contents[0], 'text')]
