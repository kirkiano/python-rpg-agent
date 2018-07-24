from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://interestingengineering.com')
def scrape_inteng(soup):
    tags = []
    for cls, get_title in (
            ('main-post-title', lambda t: t['title']),
            ('main-video-title', lambda t: t.text),
            ('featured-image', lambda t: t['title'])):
        tags += [dict(id=uuid4(), title=get_title(tag))
                 for tag in soup.find_all('a', {'class': cls})]
    return tags


SCRAPERS = [scrape_inteng]
