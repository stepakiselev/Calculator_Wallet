import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
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
        today = dt.date.today()
        return sum([
            record.amount for record in self.records
            if record.date == today
        ])

    def get_today_remained(self):
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        week_ago = dt.date.today() - dt.timedelta(days=7)
        today = dt.date.today()
        return sum([
            record.amount for record in self.records
            if week_ago < record.date <= today
        ])


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        in_my_stomach = self.get_today_remained()
        if in_my_stomach <= 0:
            return 'Хватит есть!'
        return (
            'Сегодня можно съесть что-нибудь ещё, '
            'но с общей калорийностью не более '
            f'{in_my_stomach} кКал'
        )


class CashCalculator(Calculator):
    USD_RATE = 75.83
    EURO_RATE = 91.56
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        currency_dict = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }

        if currency not in currency_dict:
            raise Exception('Такая валюта не поддерживается')
        currency_name, currency_rate = currency_dict[currency]

        spent = self.get_today_remained()
        if spent == 0:
            return 'Денег нет, держись'
        remained_money = round((spent / currency_rate), 2)
        if spent < 0:
            return (
                'Денег нет, держись: твой долг - '
                f'{abs(remained_money)} {currency_name}'
            )
        return (
            'На сегодня осталось '
            f'{remained_money} {currency_name}'
        )
