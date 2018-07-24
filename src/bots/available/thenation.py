from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://www.thenation.com')
def scrape_nation(soup):
    sayings = []
    for cls, select in (('story', lambda c: c[1][0]),
                        ('info', lambda c: c[0][0])):
        tags = soup.find_all(class_=lambda a: a and a.startswith(cls))
        says = [t.text for t in tags]
        sayings.extend(says)
    return [dict(id=uuid4(), title=s) for s in sayings]


SCRAPERS = [scrape_nation]
