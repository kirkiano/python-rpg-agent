from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_federalist():
    html = await get_web_page('https://thefederalist.com/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = [dict(id=uuid4(), title=t.text)
            for t in soup.find_all(class_='entry-title')]
    return tags


SCRAPERS = [scrape_federalist]
