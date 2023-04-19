import sqlite3


class CurrencyDatabase():
    def __init__(self):
        self._connection = sqlite3.connect("currencies")

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()

        cursor = self._connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            self._connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()

        return data

    def create(self):
        self.execute(sql="""
                           create table if not exists currency_operations(
                           id integer not null primary key,
                           date_ text not null,
                           currency text not null,
                           buy text not null,
                           sell text not null,
                           quantity text not null,
                           operation text not null,
                           received text not null 
                           );""", commit=True)

    def drop(self):
        self.execute(sql="drop table if exists currency_operations ;", commit=True)

    def select_all(self):
        return self.execute(sql="select * from currency_operations ; ", fetchall=True, commit=True)

    def insert(self, date_, currency, buy, sell, quantity, operation, received):
        self.execute(sql="""insert or ignore into 
                            currency_operations(date_,currency,buy,sell,quantity,operation,received)
                            values( :date_,:currency,:buy,:sell,:quantity,:operation,:received)""", parameters=(date_,currency,buy,sell,quantity,operation,received),commit=True)
