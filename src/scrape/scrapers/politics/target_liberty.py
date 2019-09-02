from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('http://www.targetliberty.com/')
def scrape_target_liberty(soup):
    tags = soup.find_all(class_='post-title entry-title')
    sayings = [dict(id=uuid4(), title=t.text) for t in tags]
    return sayings


SCRAPERS = [scrape_target_liberty]
