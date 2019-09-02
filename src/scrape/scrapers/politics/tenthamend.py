from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('https://tenthamendmentcenter.com')
def scrape_tenthamend(soup):
    def select(a):
        return a and a.startswith('blog-content')

    tags = [dict(id=uuid4(), title=t.text)
            for t in soup.find_all(class_=select)]
    return tags


SCRAPERS = [scrape_tenthamend]
