from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_nation():
    html = await get_web_page('https://www.thenation.com/')
    soup = BeautifulSoup(html, 'html.parser')
    sayings = []
    for cls, select in (('story', lambda c: c[1][0]),
                        ('info', lambda c: c[0][0])):
        tags = soup.find_all(class_=lambda a: a and a.startswith(cls))
        says = [t.text for t in tags]
        sayings.extend(says)
    return [dict(id=uuid4(), title=s) for s in sayings]


SCRAPERS = [scrape_nation]
