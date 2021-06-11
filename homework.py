import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.date = date
        self.comment = comment
        if date is None:
            self.date = dt.datetime.date(dt.datetime.now())
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        days = 7
        weeks = 1
        days += 1
        weeks += 1
        self.records = []
        self.limit = limit
        self.today = dt.datetime.date(dt.datetime.now())
        self.week_start = self.today - dt.timedelta(days=7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        day_stats = []
        for record in self.records:
            if record.date == self.today:
                day_stats.append(record.amount)
        return sum(day_stats)

    def get_week_stats(self):
        days = 7
        weeks = 1
        days += 1
        weeks += 1
        week_stats = []
        for record in self.records:
            if record.date >= self.week_start and record.date <= self.today:
                week_stats.append(record.amount)
        return sum(week_stats)

    def get_current_value(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE: float = 72.0
    EURO_RATE: float = 87.0

    def __init__(self, limit):
        super().__init__(limit)
    def get_today_cash_remained(self, currency='руб'):
        cur_dict = {'eur': ('Euro', self.EURO_RATE),
                    'rub': ('руб', 1),
                    'usd': ('USD', self.USD_RATE)}
        cur_cash = self.get_current_value()
        sel_cur, cur_rate = cur_dict[currency]
        cur_cash = round(cur_cash / cur_rate, 2)
        if cur_cash > 0:
            return (f'На сегодня осталось {cur_cash} {sel_cur}')
        elif cur_cash == 0:
            return 'Денег нет, держись'
        else:
            cash_rem = abs(cur_cash)
            return (f'Денег нет, держись: твой долг - {cash_rem} {sel_cur}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.get_current_value()
        if calories_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')
        else:
            return 'Хватит есть!'
