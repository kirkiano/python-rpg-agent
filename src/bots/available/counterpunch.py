from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


def scrape_counterpunch():
    html = get_web_page('http://www.counterpunch.org')
    soup = BeautifulSoup(html, 'html.parser')

    def title_then_author(tag):
        author = tag.find('left-sidebar-author').text
        title = tag.find('left-sidebar-title').text
        return f'{title}, by {author}'

    return [dict(id=uuid4(), title=title_then_author(t))
            for t in soup.find_all('div', {'class': 'left-list'})]


SCRAPERS = [scrape_counterpunch]
