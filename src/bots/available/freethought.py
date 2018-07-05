from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_freethought():
    html = await get_web_page('https://thefreethoughtproject.com/')
    soup = BeautifulSoup(html, 'html.parser')

    def select(a):
        return a and a.startswith('td_module_trending_now')

    return [dict(id=uuid4(), title=t.text)
            for t in soup.find_all('div', {'class': select})]
