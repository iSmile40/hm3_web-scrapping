import requests
from bs4 import BeautifulSoup
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

response = requests.get('https://habr.com/ru/all/')

if not response.ok:
    raise ValueError('Нет ответа')

text = response.text
soup = BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')
for article in articles:
    title_elem = article.find('a', class_='post__title_link')
    title_text = title_elem.text.strip()

    hubs = [h.text.strip().lower() for h in article.find_all('a', class_='hub-link')]
    preview = article.find('div', class_='post__text-html').text.strip().lower()

    href = title_elem.attrs.get('href')
    response_2 = requests.get(href)
    soup_2 = BeautifulSoup(response_2.text, features='html.parser')

    body_element = soup_2.find('div', class_='post__text')
    body = body_element.text.strip().lower()


    for desired in KEYWORDS:
        if desired in title_text.lower() or desired in hubs or desired in preview or desired in body:
            data_element = soup_2.find('span', class_='post__time')
            data_text = data_element.attrs.get('data-time_published')
            date_old = datetime.strptime(data_text, "%Y-%m-%dT%H:%MZ")
            data = datetime.strftime(date_old, "%d-%m-%Y")
            print(data, title_text, href)
