from bs4 import BeautifulSoup
from uuid import uuid4

from util.web import get_web_page


def download_interesting_engineering(debug=False):
    r = get_web_page('https://interestingengineering.com', debug=debug)
    soup = BeautifulSoup(r, 'html.parser')
    tags = []
    for cls, get_title in (
            ('main-post-title', lambda t: t['title']),
            ('main-video-title', lambda t: t.text),
            ('featured-image', lambda t: t['title'])):
        tags += [dict(id=uuid4(), title=get_title(t))
                 for t in soup.find_all('a', {'class': cls})]

    return tags
