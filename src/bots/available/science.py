from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_sciencemag():
    html = await get_web_page('http://www.sciencemag.org/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(class_=lambda a: a and a.startswith('media__headline'))
    headlines = [dict(id=uuid4(), title=tag.text) for tag in tags]
    return headlines
