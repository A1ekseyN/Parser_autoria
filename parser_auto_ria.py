import time
import requests
from bs4 import BeautifulSoup
import csv

start_time = time.time()

CSV = 'cars.csv'
HOST = 'https://auto.ria.com/'
#URL = 'https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&year[0].lte=1993&categories.main.id=1&brand.id[0]=9&model.id[0]=3219&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page=0&size=10'
URL = 'https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&plateNumber.length.gte=1&categories.main.id=1&brand.id[0]=84&model.id[0]=45412&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=-1&page=0&size=10'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    # Функция, которая забирает html с сервера
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    # Получаение контента из html.
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('section', class_='ticket-item')
    cars = []

    # Пробую через try/except
    #for item in items:
    #    try:
    #        cars.append({'title': item.find('div', class_='item ticket-title').get_text(strip=True)[:-4]})
            #cars.append({'plate_number': item.find('span', class_='state-num ua',).get_text(strip=True)[:-73]})
    #    except:
    #        cars.append({'title': None})
            #cars.append({'plate_number': None})
    #return cars


    for item in items:
        cars.append(
            {
                'title': item.find('div', class_='item ticket-title').get_text(strip=True)[:-4],
                'year':item.find('div', class_='item ticket-title').get_text(strip=True)[-4:],
                'car_price': item.find('div', class_='price-ticket').get('data-main-price'),
                'mileage': item.find('li', class_='item-char js-race').get_text(strip=True),
                'fuel': item.find_all('li', class_='item-char')[2].get_text(strip=True),
                'transmission': item.find_all('li', class_='item-char')[3].get_text(strip=True),
                'location': item.find('li', class_='item-char view-location js-location').get_text(strip=True)[:-5],
                'plate_number': item.find('span', class_='state-num ua').get_text(strip=True)[:-73],
                #'vin': item.find('span', class_='d-block js-VIN-code').get_text(),    ### Вин код сгенерирован с помощью картинки
                'data_add': item.find('div', class_='footer_ticket').get_text(strip=True),
                'description': item.find('p', class_='descriptions-ticket').get_text(),
                'link_car': item.find('div', class_='item ticket-title').find('a').get('href'),
                'img': item.find('img', class_='outline m-auto').get('src'),
            }
        )
    return cars


def save_data(items, path):
    # Сохранение информации в файл csv
    with open(path, 'w', encoding='utf-8',newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название машины', 'Год', 'Цена в $', 'Пробег', 'Двигатель', 'Коробка передач', 'Город', 'Номерной знак', 'Дата добавления', 'Описание', 'Ссылка на объявление', 'Фотография'])
        #writer.writerow(['Название', 'Номерной знак'])
        for item in items:
            writer.writerow([item['title'], item['year'], item['car_price'], item['mileage'], item['fuel'], item['transmission'], item['location'], item['plate_number'], item['data_add'], item['description'], item['link_car'], item['img']])
            #writer.writerow([item['title'], item['year']])


def parser():
    # Скрипт, который спрашивает сколько страниц нужно спарсить, и проходит по каждой странице по одной
    PAGENATION = input("Сколько страниц будем парсить? ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        for page in range(1, PAGENATION + 1):
            print(f"Парсим страницу: {page}. ({page / PAGENATION * 100:,.2f} %) :: ({time.time() - start_time:,.2f} sec)")
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
            save_data(cars, CSV)
        print("\n -- Парсинг закончился --")
        print(cars)
        pass
    else:
        print("Error")

parser()


#html = get_html(URL)
#print(get_content(html.text))

#get_html(URL)


# YouTube - link
#https://www.youtube.com/watch?v=ykjBVT57r68&list=PLMB6wLyKp7lWSa816Oicnp6X66oZhBrP4&index=34&ab_channel=%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B9%D0%90%D0%BD%D0%B4%D1%80%D0%B8%D0%B5%D0%B2%D1%81%D0%BA%D0%B8%D0%B9

#==================================================
print(f"\nВыполнено за: {time.time() - start_time:,.2f} секунды.")
