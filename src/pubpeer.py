import json
import urllib.request


def download_latest_from_pubpeer():
    url = 'https://pubpeer.com/api/recent'
    request = urllib.request.urlopen(url)
    jsn = json.load(request)

    return [
        dict(id=p['id'],
             title=p['title'],
             journals=set([j['title'] for j in p['journals']['data']]))
        for p in jsn['publications']
        ]
