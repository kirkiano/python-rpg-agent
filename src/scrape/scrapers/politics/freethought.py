from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://thefreethoughtproject.com')
def scrape_freethought(soup):
    return [dict(id=uuid4(), title=t.text)
            for t in soup.find_all(class_='entry-title')]


SCRAPERS = [scrape_freethought]
