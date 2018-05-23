from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_ajp():
    r = await get_web_page('https://aapt.scitation.org/journal/ajp')
    soup = BeautifulSoup(r, 'html.parser')
    tags = [dict(id=uuid4(), title=t.text)
            for t in soup.find_all(class_='title')]
    return tags
