from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('https://aapt.scitation.org/journal/ajp')
def scrape_ajp(soup):
    tags = [dict(id=uuid4(), title=t.text)
            for t in soup.find_all(class_='title')]
    return tags


SCRAPERS = [scrape_ajp]
