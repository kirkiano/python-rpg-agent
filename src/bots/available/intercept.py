from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_intercept():
    html = await get_web_page('https://theintercept.com')
    soup = BeautifulSoup(html, 'html.parser')
    tags = []
    for cls in ('HomeFeature-title', 'Promo-title'):
        tags += [dict(id=uuid4(), title=t.text)
                 for t in soup.find_all('h1', {'class': cls})]
    return tags


SCRAPERS = [scrape_intercept]
