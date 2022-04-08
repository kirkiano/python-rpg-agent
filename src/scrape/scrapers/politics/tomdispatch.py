from uuid import uuid4

from scrape import html_scraper


@html_scraper('http://www.tomdispatch.com')
def scrape_tomdispatch(soup):
    return [dict(id=uuid4(), title=tag.text)
            for tag in soup.find_all(class_='title')]


SCRAPERS = [scrape_tomdispatch]
