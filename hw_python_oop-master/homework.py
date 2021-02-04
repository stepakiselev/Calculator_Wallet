import datetime as dt
from datetime import timedelta


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is not None:
            date_format = '%d.%m.%Y'
            written_date = dt.datetime.strptime(date, date_format)
            self.date = written_date.date()
        else:
            self.date = dt.date.today()

    def show(self):
        print(f'{self.amount}, {self.comment}, {self.date}')


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def show(self):
        print(f'{self.records}')

    def get_today_stats(self):
        return sum([
            record.amount for record in self.records
            if record.date == dt.date.today()
        ])

    def get_today_remained(self):
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        week_ago = dt.date.today() - timedelta(days=7)
        return sum([
            record.amount for record in self.records
            if week_ago < record.date <= dt.date.today()
        ])


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        in_my_stomach = self.get_today_stats()
        if in_my_stomach >= self.limit:
            return 'Хватит есть!'
        elif in_my_stomach < self.limit:
            return (
                'Сегодня можно съесть что-нибудь ещё, '
                'но с общей калорийностью не более '
                f'{self.get_today_remained()} кКал'
            )


class CashCalculator(Calculator):
    USD_RATE = 75.83
    EURO_RATE = 91.56
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        dict_currency = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }

        currency_string = dict_currency[currency][0]
        rate = dict_currency[currency][1]
        spent = self.get_today_stats()
        remained_money = round((self.get_today_remained() / rate), 2)
        debt = abs(round(((self.limit - spent) / rate), 2))

        if spent == self.limit:
            return 'Денег нет, держись'
        elif spent < self.limit:
            return (
                'На сегодня осталось '
                f'{remained_money} {currency_string}'
                    )
        elif spent > self.limit:
            return (
                'Денег нет, держись: твой долг - '
                f'{debt} {currency_string}'
            )
