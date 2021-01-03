import requests
from bs4 import BeautifulSoup

URL = "https://students.bmstu.ru/schedule/list"


def get_html(url, params=None):
    r = requests.get(url, headers=None, params=params)
    return r


def get_groups(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('a', class_="btn btn-sm btn-default text-nowrap")

    return list(map(lambda x: x.text.rstrip().lstrip(), items))


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print('Page downloaded...')
    else:
        print('Error while getting html page!')

    return get_groups(html)



