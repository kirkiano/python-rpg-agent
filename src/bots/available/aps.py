from functools import partial
from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def _scrape_aps(url):
    html = await get_web_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    return [dict(id=uuid4(), title=tag['data-title'])
            for tag in soup.find_all('a', {'data-kind': 'FeaturedArticle'})]


scrape_pra = partial(_scrape_aps, 'https://journals.aps.org/pra/')
scrape_prb = partial(_scrape_aps, 'https://journals.aps.org/prb/')
scrape_prc = partial(_scrape_aps, 'https://journals.aps.org/prc/')
scrape_prd = partial(_scrape_aps, 'https://journals.aps.org/prd/')
scrape_pre = partial(_scrape_aps, 'https://journals.aps.org/pre/')
scrape_prl = partial(_scrape_aps, 'https://journals.aps.org/prl/')
scrape_prx = partial(_scrape_aps, 'https://journals.aps.org/prx/')
scrape_rmp = partial(_scrape_aps, 'https://journals.aps.org/rmp/')
scrape_prfluids = partial(_scrape_aps, 'https://journals.aps.org/prfluids/')
scrape_prapplied = partial(_scrape_aps, 'https://journals.aps.org/prapplied/')
scrape_revmodphys = partial(_scrape_aps, 'https://journals.aps.org/rmp/')
scrape_prmaterials = partial(_scrape_aps,
                             'https://journals.aps.org/prmaterials/')


async def scrape_apsnews():
    html = await get_web_page(
        'http://www.aps.org/publications/apsnews/index.cfm')
    soup = BeautifulSoup(html, 'html.parser')
    sections = soup.find_all(class_='featured-page')
    tags = []
    for section in sections:
        tags += [dict(id=uuid4(), title=tag.text)
                 for tag in section.find_all('a')]
    return tags


async def scrape_apsphysics():
    html = await get_web_page('https://physics.aps.org/')
    soup = BeautifulSoup(html, 'html.parser')
    tags = [dict(id=uuid4(), title=tag.text)
            for tag in soup.find_all(class_='feed-item-title')]
    return tags


async def scrape_physicstoday():
    url = 'http://feeds.feedburner.com/pt6dailyedition?format=sigpro'
    lines = (await get_web_page(url)).decode('utf-8').splitlines()
    quoteds = [ln[182:-26] for ln in lines[3:9:2]]
    return [dict(id=uuid4(), title=quoted) for quoted in quoteds]
