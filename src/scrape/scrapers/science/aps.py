from uuid import uuid4

from scrape import html_scraper
from scrape.util import find_all


def _scrape_aps(soup):
    return [dict(id=uuid4(), title=tag['data-title'])
            for tag in soup.find_all('a', {'data-kind': 'FeaturedArticle'})]


SCRAPERS = []

for bot_name in ('pra', 'prb', 'prc', 'prd', 'pre', 'prl', 'prx', 'rmp'):
    aps_url = 'https://journals.aps.org/' + bot_name
    scraper = html_scraper(aps_url)(_scrape_aps)
    scraper.__name__ = 'scrape_' + bot_name
    globals()[scraper.__name__] = scraper
    SCRAPERS.append(scraper)


@html_scraper('https://www.aps.org/publications/apsnews/index.cfm')
def scrape_apsnews(soup):
    tags = [dict(id=uuid4(), title=tag.text)
            for tag in soup.find_all(class_='CS_Textblock_Text')]
    return tags


@html_scraper('https://physics.aps.org')
def scrape_apsphysics(soup):
    tags = [dict(id=uuid4(), title=tag.text)
            for tag in soup.find_all(class_='feed-item-title')]
    return tags


@html_scraper('https://physicstoday.scitation.org/journal/pto')
def scrape_physicstoday(soup):
    def selector(a):
        return a and a.find('title') != -1
    return [dict(id=uuid4(), title=tag.text)
            for tag in find_all(soup, class_=selector)]


SCRAPERS += [
    scrape_apsnews,
    scrape_apsphysics,
    scrape_physicstoday,
]
