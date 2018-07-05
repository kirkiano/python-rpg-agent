from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_natrev():
    html = await get_web_page('https://www.nationalreview.com/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(class_='post-list-article__title')
    return [dict(id=uuid4(), title=t.contents[0].text) for t in tags
            if hasattr(t.contents[0], 'text')]


SCRAPERS = [scrape_natrev]
