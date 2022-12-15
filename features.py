from bs4 import BeautifulSoup
import requests
import os.path
import os
from datetime import date
from collections import namedtuple
import pandas as pd
import matplotlib.pyplot as plt


# static variables
FILE_DIR = 'crypto_files/'
URL = 'https://crypto.com/price'

# Currency object
CurrencyToday = namedtuple('CurrencyToday', ['file_name', 'file_exists'])


def is_today() -> CurrencyToday:
    """Check if file exists"""
    crypto_date = date.today()
    file_name = f'{crypto_date}.csv'
    return CurrencyToday(file_name, os.path.isfile(FILE_DIR + file_name))


def scrap_data(f):
    """Scrap data and write to given file"""
    req = requests.get(URL).text
    document = BeautifulSoup(req, 'lxml')
    pages = int(list(document.find(class_='css-b6hlml').children)[-3].text)

    for page in range(1, pages + 1):
        url = f'https://crypto.com/price?page={page}'
        req = requests.get(url).text
        document = BeautifulSoup(req, 'lxml')
        cryptocurrency = document.find_all(class_='css-1cxc880')

        for currency in cryptocurrency:
            name = currency.find(class_='chakra-text css-rkws3').string
            short_name = currency.find(class_='chakra-text css-1jj7b1a').string
            price = currency.find(class_='css-b1ilzc').string.replace(',', '')
            f.write(f'{name},{short_name},{price}\n')


def create_crypto_csv():
    """Scraps data from given url and writes to csv file"""
    file_name = is_today().file_name

    if not is_today().file_exists:
        with open(FILE_DIR + file_name, 'w') as file:
            scrap_data(file)
            print('File successfully created')
    else:
        print(f'File {file_name} exists')


def read_crypto_csv(name: str) -> list:
    """Creates list with data for a given cryptocurrency"""
    crypto_list = []

    for root, dirs, files in os.walk(FILE_DIR):
        for file in sorted(files):
            with open(FILE_DIR + file, 'r') as crypto:
                for line in crypto.readlines():
                    if name == line.split(',')[0] or name == line.split(',')[1]:
                        crypto_list.append(f'{line.strip()},{file[0:-4]}')

    return crypto_list


def draw_chart(name: str):
    """Draw chart"""
    clist = read_crypto_csv(name)

    if clist:
        chart_data = {'Date': [], 'Name': [], 'Short_Name': [], 'Price': []}

        for crypto in clist:
            if len(crypto.split(',')) == 4:
                price_date = crypto.split(',')[3]
                crypto_name = crypto.split(',')[0]
                short_name = crypto.split(',')[1]
                price = crypto.split(',')[2][1:]
            elif len(crypto.split(',')) == 5:
                price_date = crypto.split(',')[4]
                crypto_name = crypto.split(',')[0]
                short_name = crypto.split(',')[1] + ',' + crypto.split(',')[2]
                price = crypto.split(',')[3][1:]

            chart_data['Date'].append(price_date)
            chart_data['Name'].append(crypto_name)
            chart_data['Short_Name'].append(short_name)
            chart_data['Price'].append(float(price))

        chart = pd.DataFrame(chart_data, columns=['Date', 'Name', 'Short_Name', 'Price'])

        plt.style.use('fivethirtyeight')
        plt.figure(figsize=(12, 10))
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'{crypto_name}({short_name})')

        plt.plot(chart['Date'], chart['Price'])
        plt.show()
    else:
        print('No such cryptocurrency')
