from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://www.wsws.org/')
def scrape_world_socialist(soup):
    tags = soup.find_all(class_='noborder')
    sayings = [dict(id=uuid4(), title=t.text) for t in tags]
    return sayings


SCRAPERS = [scrape_world_socialist]
