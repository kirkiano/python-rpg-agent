from uuid import uuid4

from scrape.decorators import html_scraper


@html_scraper('http://ronpaulinstitute.org')
def scrape_ronpaul(soup):
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
