from bs4 import BeautifulSoup
from uuid import uuid4

from util.web import get_web_page


def download_retraction_watch(debug=False):
    r = get_web_page('https://retractionwatch.com/', debug=debug)
    soup = BeautifulSoup(r, 'html.parser')
    tags = soup.find_all(class_='entry-title')
    return [dict(id=uuid4(), title=t.contents[0].text) for t in tags]