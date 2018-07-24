from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://www.counterpunch.org')
def scrape_counterpunch(soup):
    def title_then_author(tag):
        author = tag.find(class_='left-sidebar-author').text
        title = tag.find(class_='left-sidebar-title').text
        return f'{title}, by {author}'

    return [dict(id=uuid4(), title=title_then_author(t))
            for t in soup.find_all('div', {'class': 'left-list'})]


SCRAPERS = [scrape_counterpunch]
