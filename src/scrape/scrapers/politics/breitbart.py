from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://www.breitbart.com')
def scrape_breitbart(soup):
    tags = soup.find_all('article')
    tags.extend(soup.find_all('div', {'id': 'BBTrendNow'}))
    sayings = [dict(id=uuid4(), title=t.text) for t in tags]
    return sayings


SCRAPERS = [scrape_breitbart]
