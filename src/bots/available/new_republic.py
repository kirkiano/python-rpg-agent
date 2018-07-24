from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://newrepublic.com')
def scrape_newrep(soup):
    tags = soup.find_all(class_='card-title')
    sayings = []
    for tag in tags:
        c = tag.contents
        title = c[0].text if hasattr(c[0], 'text') else ''
        subtitle = c[1].text if len(c) > 1 and hasattr(c[1], 'text') else ''
        full = title + (': ' + subtitle if subtitle else '')
        sayings.append(dict(id=uuid4(), title=full))
    return sayings


SCRAPERS = [scrape_newrep]
