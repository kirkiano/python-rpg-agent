from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://thefreethoughtproject.com')
def scrape_freethought(soup):
    def select(a):
        return a and a.startswith('td_module_trending_now')

    return [dict(id=uuid4(), title=t.text)
            for t in soup.find_all('div', {'class': select})]
