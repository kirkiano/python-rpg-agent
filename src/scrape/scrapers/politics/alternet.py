from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://www.alternet.org')
def scrape_alternet(soup):
    tags = soup.find_all('div', {'class': 'title_overlay'})
    lines = [dict(id=uuid4(), title=t.text) for t in tags]
    return lines


SCRAPERS = [scrape_alternet]
