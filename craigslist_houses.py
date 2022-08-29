
import requests
from bs4 import BeautifulSoup
import pandas as pd

city = input('City: ')
print('Note the page start from 120, 360, 480....and so on')
page = int(input('Number of page to scrape: '))

n = []
p = []
post = []
house = []
address = []


def parse(url):
    response = requests.get(url, timeout=50000)
    soup = BeautifulSoup(response.text, 'lxml')
    box = soup.find_all('li', {'class': 'result-row'})
    for b in box:
        link_way = b.find('h3', {'class': 'result-heading'})
        link = link_way.find('a', {'class': 'result-title hdrlnk'})['href']
        detailed_page(link)


def pagination():
    for x in range(0, page, 120):
        print(f'Page {x}')
        nxt = f'https://{city}.craigslist.org/search/hhh?s={x}'
        parse(nxt)


def detailed_page(link):
    res = requests.get(link)
    soup2 = BeautifulSoup(res.text, 'lxml')
    try:
        name = soup2.find('span', {'id': 'titletextonly'}).text
        n.append(name)
    except:
        n.append('')
    try:
        price = soup2.find('span', {'class': 'price'}).text
        p.append(price)
    except:
        p.append('')
    try:
        posted = soup2.find('time', {'class': 'date timeago'}).text.strip()
        post.append(posted)
    except:
        post.append('')
    try:
        housing = soup2.find('span', {'class': 'housing'}).text.strip()
        house.append(housing)
    except:
        house.append('')
    try:
        add = soup2.find('div', {'class': 'mapaddress'}).text
        address.append(add)
    except:
        address.append('')


pagination()
df = pd.DataFrame({
    'House Name': n,
    "House Price": p,
    'Posted Date': post,
    'About House': house,
    'Map Address': address
})
df.to_csv('craigslist.csv')
df