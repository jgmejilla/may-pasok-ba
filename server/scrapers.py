from bs4 import BeautifulSoup
import requests
from datetime import datetime

RAPPLER = 'https://www.rappler.com/latest/'
RAPPLER_ALT = 'https://www.rappler.com/topic/class-suspensions'

def rappler():
    response = requests.get(RAPPLER)
    page = response.text

    soup = BeautifulSoup(page, 'html.parser')

    main = soup.body.main

    articles = []
    for headline in main.select('article'):
        content = headline.find('div', class_='archive-article__content')
        header = content.find(['h2', 'h3'])
        anchor = header.a
        link = anchor['href'].strip()
        title = anchor.text.strip()

        articles.append({"title": title, "link": link, "source": "rappler"})

    return articles




    