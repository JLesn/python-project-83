import requests
from bs4 import BeautifulSoup


def check_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    status_code = r.status_code
    h1 = soup.find('h1').getText() if soup.find('h1') else ''
    title = soup.find('title').getText() if soup.find('title') else ''
    find_description = soup.find('meta', attrs={'name': 'description'})
    if find_description:
        description = find_description.get('content', '')
    else:
        description = ''
    return {
        'status_code': status_code,
        'h1': h1,
        'title': title,
        'description': description
    }
