from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_ronpaul():
    html = await get_web_page('https://ronpaulinstitute.org/')
    soup = BeautifulSoup(html, 'html.parser')
    sayings = []

    tags = soup.find_all(id='featured-article')
    sayings.extend([t.contents[1].text for t in tags])

    tags = soup.find_all(class_='featuredsub')
    sayings.extend([t.contents[1].text for t in tags])

    tags = soup.find_all(id_='twocolumnmedia')
    sayings.extend([t.contents[1].text for t in tags])

    tags = soup.find_all(class_='ppblog-posts')
    sayings.extend([t.contents[1].text for t in tags])

    tags = soup.find_all(id_='rightsidebar')
    for tag in tags:
        subtags = tag.find_all('strong')
        sayings.extend(t.contents[0].text for t in subtags)

    return [dict(id=uuid4(), title=s) for s in sayings]


SCRAPERS = [scrape_ronpaul]
