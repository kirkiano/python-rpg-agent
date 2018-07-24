from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://www.commondreams.org')
def scrape_commondreams(soup):
    return [dict(id=uuid4(), title=t.text.strip())
            for t in
            (soup
             .find('div', {'class': 'hide-for-desktop'})
             .find_all('div', {'class': 'views-field-field-hp-title'}))]


SCRAPERS = [scrape_commondreams]
