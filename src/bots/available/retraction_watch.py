from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_retwatch():
    html = await get_web_page('https://retractionwatch.com/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(class_='entry-title')
    return [dict(id=uuid4(), title=tags.contents[0].text) for tags in tags
            if hasattr(tags.contents[0], 'text')]


SCRAPERS = [scrape_retwatch]
