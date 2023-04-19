import copy
import re
import time
from threading import Lock

import requests
from bs4 import BeautifulSoup


class Currencies:
    currencies_names = [
        'usd',
        'eur',
        'chf',
        'pln',
        'huf',
        'czk',
        'sek',
        'nok',
        'dkk',
        'aud',
        'cad',
        'jpy',
        'gbp'
    ]
    currencies_description = {
        'usd': 'Доллар США',
        'eur': 'Євро',
        'chf': 'Швейцарский франк',
        'pln': 'Польский злотий',
        'huf': 'Венгерский форинт',
        'czk': 'Чеська крона',
        'sek': 'Шведська крона',
        'nok': 'Норвежська крона',
        'dkk': 'Датська крона ',
        'aud': 'Австралійский доллар',
        'cad': 'Канадский доллар',
        'jpy': 'Японська єна',
        'gbp': 'Фунт стерлинга'
    }

    def __init__(self):
        self.currencies: dict = dict()

    def get_currencies(self):
        lock = Lock()
        lock.acquire()
        while True:
            for currency in self.currencies_names:
                soup = BeautifulSoup(requests.get(f'https://kurs.com.ua/valyuta/{currency}').content, 'html.parser')
                find_currency = soup.find_all('div', {'class': 'course'})
                buy, sell = re.sub(r'(\n.+\n|\n\n)', "", find_currency[0].text).replace(",", "."), re.sub(
                    r'(\n.+\n|\n\n)', "",
                    find_currency[1].text).replace(",", ".")
                if buy == "---" or sell == "---":
                    continue

                buy_copy,sell_copy = copy.deepcopy(buy),copy.deepcopy(sell)
                if buy.count(".") >= 2:
                    buy_copy = buy[:3:]
                if sell.count(".") >= 2:
                    sell_copy = sell[:3:]
                self.currencies[f'{currency}'] = {'buy': buy_copy, 'sell': sell_copy}

            time.sleep(600)
            lock.release()
