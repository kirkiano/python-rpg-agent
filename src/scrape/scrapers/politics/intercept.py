from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://theintercept.com')
def scrape_intercept(soup):
    tags = []
    for cls in ('HomeFeature-title', 'Promo-title'):
        tags += [dict(id=uuid4(), title=t.text)
                 for t in soup.find_all('h1', {'class': cls})]
    return tags


SCRAPERS = [scrape_intercept]
