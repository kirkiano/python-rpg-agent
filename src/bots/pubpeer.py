import json
import urllib.request


def scrape_pubpeer():
    url = 'https://pubpeer.com/api/recent'
    with urllib.request.urlopen(url) as f:
        jsn = json.loads(f.read().decode())

        tags = [
            dict(id=p['id'],
                 title=p['title'],
                 journals=set([j['title'] for j in p['journals']['data']]))
            for p in jsn['publications']
            ]
        return tags
