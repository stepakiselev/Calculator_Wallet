import datetime as dt
from datetime import timedelta


class Record:

    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        self.date = date
        moment_now = dt.datetime.now()
        if len(date) != 0:
            date_format = '%d.%m.%Y'
            written_date = dt.datetime.strptime(date, date_format)
            self.date = written_date.date()
        else:
            self.date = moment_now.date()

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
        total = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if record.date == today:
                total += record.amount
        return total

    def get_remained(self):
        remained_today = 0
        total_today = 0
        today = dt.datetime.now()
        for record in self.records:
            if record.date == today.date():
                total_today += record.amount
                remained_today = self.limit - total_today
        return remained_today

    def get_week_stats(self):
        total_week = 0
        today = dt.datetime.now()
        seven_days_before = (today.date() - timedelta(7))
        for record in self.records:
            if record.date <= today.date() and record.date > seven_days_before:
                total_week += record.amount
        return total_week


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        if super().get_today_stats() < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё, ' \
                   f'но с общей калорийностью не более {super().get_remained()} кКал'
        elif super().get_today_stats() >= self.limit:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 75.83
    EURO_RATE = 91.56
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency=''):
        remained_money = super().get_remained()
        spent = super().get_today_stats()
        debt = self.limit - spent
        rate = int
        currency_string = str
        if len(currency) == 0 or currency == 'rub':
            rate = self.RUB_RATE
            currency_string = 'руб'
        elif currency == 'usd':
            rate = self.USD_RATE
            currency_string = 'USD'
        elif currency == 'eur':
            rate = self.EURO_RATE
            currency_string = 'Euro'

        if spent < self.limit:
            return f'На сегодня осталось ' \
                   f'{round((remained_money / rate), 2)} {currency_string}'
        elif spent == self.limit:
            return 'Денег нет, держись'
        elif spent > self.limit:
            return f'Денег нет, держись: ' \
                   f'твой долг - {abs(round((debt / rate), 2))} {currency_string}'
