from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://reason.com')
def scrape_reason(soup):
    posts = soup.find('div', {'id': 'featured_posts'})
    return [dict(id=uuid4(), title=t.find('h3').text.strip())
            for t in posts.find_all('li', {'class': 'post'})]


SCRAPERS = [scrape_reason]
