from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_tenthamend():
    html = await get_web_page('https://tenthamendmentcenter.com/')
    soup = BeautifulSoup(html, 'html.parser')

    def select(a):
        return a and a.startswith('blog-content')

    tags = [dict(id=uuid4(), title=t.text)
            for t in soup.find_all(class_=select)]
    return tags


SCRAPERS = [scrape_tenthamend]
