from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://retractionwatch.com')
def scrape_retwatch(soup):
    tags = soup.find_all(class_='entry-title')
    return [dict(id=uuid4(), title=tags.contents[0].text) for tags in tags
            if hasattr(tags.contents[0], 'text')]


SCRAPERS = [scrape_retwatch]
