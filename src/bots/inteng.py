from bs4 import BeautifulSoup
from uuid import uuid4

from util.web import get_web_page


def download_interesting_engineering(debug=False):
    r = get_web_page('https://interestingengineering.com', debug=debug)
    soup = BeautifulSoup(r, 'html.parser')
    tags = []
    for cls in ('main-post-title', 'main-video-title', 'featured-image'):
        tags += soup.find_all('a', {'class': cls})
    return [dict(id=uuid4(), title=t['href']) for t in tags]
