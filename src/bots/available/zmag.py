from uuid import uuid4

from scraper import html_scraper


@html_scraper('https://zcomm.org/zmag')
def scrape_zmag(soup):
    widgets = soup.find_all('div', {'class': 'zmagwidget'})
    [current_zmag] = [w for w in widgets
                      if w.find('h5') and
                      w.find('h5').text.lower() == 'current zmag']
    return [dict(id=uuid4(), title=' '.join(t.text.split('\n\t')))
            for t in current_zmag.find_all('div', {'class': 'zmagtoctitles'})]


SCRAPERS = [scrape_zmag]
