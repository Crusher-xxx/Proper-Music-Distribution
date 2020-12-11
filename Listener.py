import datetime
import datetime_to_dict as dtd
import money_distribution
import copy


class MonthlyReport:
    def __init__(self, price=150):
        self.money = price
        self.been_listening_to = {}
        self.subscription_activation_date = None
        self.subscription_expiration_date = None

    def __iter__(self):  # Представить класс в виде словаря
        yield 'money', self.money
        yield 'been_listening_to', self.been_listening_to
        yield 'subscription_activation_date', dtd.get_datetime_as_dict(self.subscription_activation_date)
        yield 'subscription_expiration_date', dtd.get_datetime_as_dict(self.subscription_expiration_date)

    def get_statistics(self):  # Вернуть историю прослушивания в виде строки
        statistics = ''
        if self.subscription_activation_date is None:
            statistics += f'Статистика отсутствует'
        else:
            statistics += f'Статистика с {self.subscription_activation_date} по {self.subscription_expiration_date}\n'\
                          f'Стоимость подписки: {self.money}\n' +\
                          '{:<25} {:<10} {:<10}'.format('Музыкант', 'Время', 'Доля')

            for musician, time, share in zip(self.been_listening_to.keys(),
                                             self.been_listening_to.values(),
                                             money_distribution.distribution_income(self.been_listening_to,
                                                                                    self.money).values()):
                statistics += '\n{:<25} {:<10} {:<10}'.format(musician, time, share)

        return statistics


class Listener:
    def __init__(self, ID, name, gender):
        self.ID = ID
        self.name = name
        self.gender = gender
        self.creation_date = datetime.datetime.now()
        self.current_period: MonthlyReport = MonthlyReport(150)
        self.listening_history: list[MonthlyReport] = []

    def __eq__(self, other):
        return self.ID == other.ID \
               and self.name == other.name \
               and self.gender == other.gender \
               and self.creation_date == other.creation_date \
               and self.get_history_as_list_of_dict() == other.get_history_as_list_of_dict() \
               and dict(self.current_period) == dict(other.current_period)

    def get_history_as_list_of_dict(self):  # Представить список классов в виде списка словарей
        list_of_dict = []
        for period in self.listening_history:
            list_of_dict.append(dict(period))
        return list_of_dict

    @classmethod
    def from_dictionary(cls, dictionary):  # Восстановить слушателя из словаря
        def dict_to_datetime(dictionary):  # Восстановить дату из словаря
            if dictionary is None:
                return None
            else:
                return datetime.datetime(dictionary['year'],
                                         dictionary['month'],
                                         dictionary['day'],
                                         dictionary['hour'],
                                         dictionary['minute'],
                                         dictionary['second'],
                                         dictionary['microsecond'])

        # Восстановить простые поля
        listener = cls.__new__(cls)
        listener.name = dictionary['name']
        listener.ID = dictionary['ID']
        listener.gender = dictionary['gender']
        listener.creation_date = dict_to_datetime(dictionary['creation_date'])

        # Восстановить текущий период
        listener.current_period = MonthlyReport()
        listener.current_period.money = dictionary['current_period']['money']
        listener.current_period.been_listening_to = dictionary['current_period']['been_listening_to']
        listener.current_period.subscription_activation_date = \
            dict_to_datetime(dictionary['current_period']['subscription_activation_date'])
        listener.current_period.subscription_expiration_date = \
            dict_to_datetime(dictionary['current_period']['subscription_expiration_date'])

        # Восстановить историю
        listener.listening_history = []
        for report in dictionary['listening_history']:
            period = MonthlyReport()
            period.money = report['money']
            period.been_listening_to = report['been_listening_to']
            period.subscription_activation_date = dict_to_datetime(report['subscription_activation_date'])
            period.subscription_expiration_date = dict_to_datetime(report['subscription_expiration_date'])
            listener.listening_history.append(period)

        return listener

    def __iter__(self):  # Представить класс в виде словаря
        yield 'ID', self.ID
        yield 'name', self.name
        yield 'gender', self.gender
        yield 'creation_date', dtd.get_datetime_as_dict(self.creation_date)
        yield 'current_period', dict(self.current_period)
        yield 'listening_history', self.get_history_as_list_of_dict()

    def get_subscription_status(self):  # Вернуть текущий статус подписки
        if self.current_period.subscription_activation_date is None:
            return 'never'
        elif self.current_period.subscription_expiration_date <= datetime.datetime.now():
            return 'expired'
        else:
            return 'active'

    def activate_subscription(self):  # Продлить подписку
        if self.get_subscription_status() != 'active':
            if self.get_subscription_status() != 'never':  # Если подписка уже была
                # Добавить отчет за предыдущий период в историю
                self.listening_history.append(copy.deepcopy(self.current_period))
            self.current_period = MonthlyReport(150)  # Сбросить текущий период
            self.current_period.subscription_activation_date = datetime.datetime.now()
            self.current_period.subscription_expiration_date = \
                self.current_period.subscription_activation_date + datetime.timedelta(days=30)

    def get_subscription_report(self):  # Вернуть отчет о состоянии подписки в виде строки
        if self.get_subscription_status() == 'active':
            return f'Подписка действует до {self.current_period.subscription_expiration_date}\n'\
                   f'Осталось: {self.current_period.subscription_expiration_date - datetime.datetime.now()}'
        elif self.get_subscription_status() == 'expired':
            return f'Подписка закончилась {self.current_period.subscription_expiration_date}\n'\
                   f'Без подписки: {datetime.datetime.now() - self.current_period.subscription_expiration_date}'
        else:
            return f'Никогда не было подписки'

    def get_report(self):  # Вернуть всю статистику по пользователю в виде строки
        report = ''
        report += f'Пользователь {self.name}[{self.ID}] зарегистрирован {self.creation_date}\n'\
                  f'{self.get_subscription_report()}\n'\
                  f'{self.current_period.get_statistics()}\n'

        for x in reversed(self.listening_history):
            report += x.get_statistics() + '\n'

        return report

    def add_listening_time(self, musician, listening_time):
        if musician in self.current_period.been_listening_to:
            self.current_period.been_listening_to[musician] += listening_time
        else:
            self.current_period.been_listening_to[musician] = listening_time
