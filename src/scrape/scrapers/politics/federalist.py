from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://thefederalist.com')
def scrape_federalist(soup):
    tags = [dict(id=uuid4(), title=t.text)
            for t in soup.find_all(class_='entry-title')]
    return tags


SCRAPERS = [scrape_federalist]
