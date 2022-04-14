import aiohttp


async def download_web_page(url):
    """
    Download web content.

    Args:
        url (str): URL to fetch

    Returns:
        bytes: the body of the HTTP response
    """
    headers = {
        'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0)'
                       ' Gecko/20100101 Firefox/55.0'),
        'Accept': ('text/html,application/xhtml+xml,application/xml;'
                   'q=0.9,*/*;q=0.8'),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-CharRequests': '1',
    }
    async with aiohttp.request('GET', url, headers=headers) as resp:
        content = await resp.content.read()
        return content
