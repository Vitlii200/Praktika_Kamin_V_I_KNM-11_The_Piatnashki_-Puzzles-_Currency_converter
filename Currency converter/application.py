import datetime
import re
from threading import Thread

from prettytable import PrettyTable

from src import commands, Currencies, CurrencyDatabase


class Application:

    @staticmethod
    def run():

        updatable_currency = Currencies()

        currency_db = CurrencyDatabase()
        currency_db.create()
        loop_currencies = Thread(target=updatable_currency.get_currencies)
        loop_currencies.start()
        help_ = """
Програма для купівлі та продажу валют
Команди :
show                 Показ валют та цін валют       
exchange             Обмін
history              Історія Обмінів
exit                 Вихід з програми 
help                 Довідка про програму
        """
        currencies_list = "Доступні валюти \n"
        for currency_description in updatable_currency.currencies_description:
            currencies_list += f"{currency_description}   {updatable_currency.currencies_description[currency_description]} \n"

        currencies_list += "!!! Деякі валюти можуть бути тимчасово недоступні !!!\n Перегляньне доступні валюти за допомогою команди \"show\"\n"

        print(help_)
        print(currencies_list)


        def print_currency():
            pt_show = PrettyTable(['Валюта', 'Купівля', 'Продаж'])
            updatable_currency_temp = updatable_currency.currencies
            for currency_row in updatable_currency_temp:
                items = updatable_currency_temp[currency_row]
                pt_show.add_row([currency_row, items['buy'], items['sell']])
            print(pt_show)
        user = input("Ваше ім'я : ")
        while True:
            command = input(f"{user} -> ")
            if commands.show.match(command):
                print_currency()
            elif commands.exit_.match(command):
                loop_currencies.join()
                break
            elif commands.history.match(command):
                pt_history = PrettyTable(['№', 'Дата', 'Валюта', 'Купівля', 'Продаж', 'Кількість', 'Операція','Отримано'])
                history_list = currency_db.select_all()
                for currency_history in history_list:
                    pt_history.add_row([currency_history[0],
                                        currency_history[1],
                                        currency_history[2],
                                        currency_history[3],
                                        currency_history[4],
                                        currency_history[5],
                                        currency_history[6],
                                        currency_history[7]])

                print(pt_history)

            elif commands.exchange.match(command):
                print_currency()
                read_currency = input("Введіть валюту скороченим іменем : ").strip()
                if read_currency not in updatable_currency.currencies_names:
                    print("Неправельно введена назва валюти ")
                else:
                    buy_or_sale = input("операція купівлі чи продажу (1-купівля, 2-продажу) ? : ")
                    while buy_or_sale.strip() not in ['1', '2']:
                        buy_or_sale = input(
                            "Неправельна відповідь.Операція купівлі чи продажу (1-купівля, 2-продажу) ? : ")

                    money_regex = re.compile(r'^(?!0\d)\d*(\.\d+)?$')

                    quantity = input("Введіть кількість валюти : ")
                    while not money_regex.match(quantity):
                        quantity = input(" Неправильно . Введіть кількість валюти : ")

                    if buy_or_sale == "1":
                        currency_db.insert(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"),
                                           read_currency,
                                           updatable_currency.currencies[read_currency]['buy'],
                                           updatable_currency.currencies[read_currency]['sell'],
                                           quantity,
                                           "buy",
                                           float(quantity) * float(updatable_currency.currencies[read_currency]['buy']))
                        print(f"Операція пройшла успішно ,ви купили {float(quantity) * float(updatable_currency.currencies[read_currency]['buy'])} uah")
                    else:
                        currency_db.insert(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"),
                                           read_currency,
                                           updatable_currency.currencies[read_currency]['buy'],
                                           updatable_currency.currencies[read_currency]['sell'],
                                           quantity,
                                           "sell",
                                           round(float(quantity)/float(updatable_currency.currencies[read_currency]['sell']),2))
                        print(f"Операція пройшла успішно ,ви купили {round(float(quantity)/float(updatable_currency.currencies[read_currency]['sell']),2)}  {read_currency}")


            elif commands.help_.match(command):
                print(help_)

            else:
                print(f"Не існує команди {command}")

        loop_currencies.join()
