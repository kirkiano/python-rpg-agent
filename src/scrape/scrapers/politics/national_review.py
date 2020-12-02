from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://www.nationalreview.com')
def scrape_natrev(soup):
    tags = soup.find_all(class_='post-list-article__title')
    return [dict(id=uuid4(), title=t.contents[0].text) for t in tags
            if hasattr(t.contents[0], 'text')]


SCRAPERS = [scrape_natrev]
