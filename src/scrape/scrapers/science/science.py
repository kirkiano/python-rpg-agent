from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://www.sciencemag.org')
def scrape_sciencemag(soup):

    def selector(a):
        return a and a.startswith('media__headline')

    tags = soup.find_all(class_=selector)
    headlines = [dict(id=uuid4(), title=tag.text) for tag in tags]
    return headlines


SCRAPERS = [scrape_sciencemag]
