import requests


def get_web_page(url, data=None, debug=False):
    data = data or {}
    headers = {
        'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0)'
                       ' Gecko/20100101 Firefox/55.0'),
        'Accept': ('text/html,application/xhtml+xml,application/xml;'
                   'q=0.9,*/*;q=0.8'),
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    if data:
        r = requests.post(url, headers=headers, data=data)
    else:
        r = requests.get(url, headers=headers)
    if debug:
        print(r.status_code, r.reason)
        print(r.headers)
    return r.content
