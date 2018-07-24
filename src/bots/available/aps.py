from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page
from common import named_partial
from scraper import html_scraper


async def _scrape_aps(url):
    html = await get_web_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    return [dict(id=uuid4(), title=tag['data-title'])
            for tag in soup.find_all('a', {'data-kind': 'FeaturedArticle'})]


scrape_pra = named_partial(_scrape_aps, 'https://journals.aps.org/pra')
scrape_prb = named_partial(_scrape_aps, 'https://journals.aps.org/prb')
scrape_prc = named_partial(_scrape_aps, 'https://journals.aps.org/prc')
scrape_prd = named_partial(_scrape_aps, 'https://journals.aps.org/prd')
scrape_pre = named_partial(_scrape_aps, 'https://journals.aps.org/pre')
scrape_prl = named_partial(_scrape_aps, 'https://journals.aps.org/prl')
scrape_prx = named_partial(_scrape_aps, 'https://journals.aps.org/prx')
scrape_rmp = named_partial(_scrape_aps, 'https://journals.aps.org/rmp')
scrape_prfluids = named_partial(_scrape_aps,
                                'https://journals.aps.org/prfluids')
scrape_prapplied = named_partial(_scrape_aps,
                                 'https://journals.aps.org/prapplied')
scrape_prmaterials = named_partial(_scrape_aps,
                                   'https://journals.aps.org/prmaterials')


@html_scraper('https://www.aps.org/publications/apsnews/index.cfm')
def scrape_apsnews(soup):
    sections = soup.find_all(class_='featured-page')
    tags = []
    for section in sections:
        tags += [dict(id=uuid4(), title=tag.text)
                 for tag in section.find_all('a')]
    return tags


@html_scraper('https://physics.aps.org')
def scrape_apsphysics(soup):
    tags = [dict(id=uuid4(), title=tag.text)
            for tag in soup.find_all(class_='feed-item-title')]
    return tags


async def scrape_physicstoday():
    url = 'https://feeds.feedburner.com/pt6dailyedition?format=sigpro'
    lines = (await get_web_page(url)).decode('utf-8').splitlines()
    quoteds = [ln[182:-26] for ln in lines[3:9:2]]
    return [dict(id=uuid4(), title=quoted) for quoted in quoteds]


SCRAPERS = [
    scrape_pra,
    scrape_prb,
    scrape_prc,
    scrape_prd,
    scrape_pre,
    scrape_prl,
    scrape_prx,
    scrape_rmp,
    scrape_prfluids,
    scrape_prapplied,
    scrape_prmaterials,
    scrape_apsnews,
    scrape_apsphysics,
    scrape_physicstoday,
]
