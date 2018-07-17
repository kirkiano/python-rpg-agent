from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_reason():
    html = await get_web_page('https://reason.com')
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.find('div', {'id': 'featured_posts'})
    return [dict(id=uuid4(), title=t.find('h3').text.strip())
            for t in posts.find_all('li', {'class': 'post'})]


SCRAPERS = [scrape_reason]
