from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_commondreams():
    html = await get_web_page('https://www.commondreams.org')
    soup = BeautifulSoup(html, 'html.parser')
    return [dict(id=uuid4(), title=t.text.strip())
            for t in
            (soup
             .find('div', {'class': 'hide-for-desktop'})
             .find_all('div', {'class': 'views-field-field-hp-title'}))]


SCRAPERS = [scrape_commondreams]
