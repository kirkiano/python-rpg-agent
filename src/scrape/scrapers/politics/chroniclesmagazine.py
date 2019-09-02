from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('https://chroniclesmagazine.org')
def scrape_chroniclesmagazine(soup):
    contents = soup.find_all('div', {'class': 'content'})
    slide_infos = soup.find_all('div', {'class': 'slideInfo'})
    tags = contents + slide_infos
    return [dict(id=uuid4(), title=t.text) for t in tags]


SCRAPERS = [scrape_chroniclesmagazine]
