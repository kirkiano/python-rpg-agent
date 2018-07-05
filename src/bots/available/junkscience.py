from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_junkscience():
    html = await get_web_page('https://junkscience.com')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('h2', {'class': 'entry-title'})
    return [dict(id=uuid4(), title=t.text) for t in tags]


SCRAPERS = [scrape_junkscience]
