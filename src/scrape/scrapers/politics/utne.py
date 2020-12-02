from uuid import uuid4

from scrape import html_scraper


@html_scraper('https://www.utne.com')
def scrape_utne(soup):
    return [dict(id=uuid4(), title=t.text.strip()) for t in
            soup.find_all('div', {'class': 'catLandingFeaturedContent'})]


SCRAPERS = [scrape_utne]
