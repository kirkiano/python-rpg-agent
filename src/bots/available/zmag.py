from uuid import uuid4

from bs4 import BeautifulSoup

from web import get_web_page


async def scrape_zmag():
    html = await get_web_page('https://zcomm.org/zmag')
    soup = BeautifulSoup(html, 'html.parser')
    widgets = soup.find_all({'class': 'zmagwidget'})
    [current_zmag] = [w for w in widgets
                      if w.find('h5') and
                      w.find('h5').text.lower() == 'current zmag']
    return [dict(id=uuid4(), title=' '.join(*t.text.split('\n\t')))
            for t in current_zmag.find_all('div', {'class': 'zmagtoctitles'})]


SCRAPERS = [scrape_zmag]
