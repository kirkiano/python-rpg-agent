from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_alternet():
    html = await get_web_page('https://www.alternet.org')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('div', {'class': 'title_overlay'})
    lines = [dict(id=uuid4(), title=t.text) for t in tags]
    return lines


SCRAPERS = [scrape_alternet]
