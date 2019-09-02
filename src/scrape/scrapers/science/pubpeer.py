from scrape.decorators import json_scraper


@json_scraper('https://pubpeer.com/api/recent')
def scrape_pubpeer(json_content):
    tags = [
        dict(id=pub['id'],
             title=pub['title'],
             journals=set([jrn['title']
                           for jrn in pub['journals']['data']]))
        for pub in json_content['publications']
    ]
    return tags


SCRAPERS = [scrape_pubpeer]
