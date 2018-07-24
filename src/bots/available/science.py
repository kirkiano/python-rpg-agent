from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://www.sciencemag.org')
def scrape_sciencemag(soup):
    tags = soup.find_all(class_=lambda a: a and a.startswith('media__headline'))
    headlines = [dict(id=uuid4(), title=tag.text) for tag in tags]
    return headlines


SCRAPERS = [scrape_sciencemag]
