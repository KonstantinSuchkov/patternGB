import json
import abc

SOLID = ['SOLID - это аббревиатура 5-ти основных принципов проектирования в объектно-ориентированном программировании',
         "1. Принцип единственной ответственности (single responsibility principle). Для каждого класса должно быть "
         "определено единственное назначение. Все ресурсы, необходимые для его осуществления, должны быть "
         "инкапсулированы в этот класс и подчинены только этой задаче",
         "2. Принцип открытости/закрытости (open-closed principle). Программные сущности … должны быть открыты для "
         "расширения, но закрыты для модификации",
         "3. Принцип подстановки Лисков (Liskov substitution principle). Функции, которые используют базовый тип, "
         "должны иметь возможность использовать подтипы базового типа не зная об этом",
         "4. Принцип разделения интерфейса (interface segregation principle). Много интерфейсов, специально "
         "предназначенных для клиентов, лучше, чем один интерфейс общего назначения",
         "5. Принцип инверсии зависимостей (dependency inversion principle). Зависимость на Абстракциях. Нет "
         "зависимости на что-то конкретное"]


def save_data(params, dict_name):
    """
    :param params: что сохраняем
    :param dict_name: имя раздела словаря, куда сохраняем (например, "GET" или "POST")
    :return:
    """
    with open('data.json', 'r', encoding='utf-8') as f_r:
        data = json.load(f_r)

    with open('data.json', 'w', encoding='utf-8') as f_w:
        order = data[dict_name]
        order.append(params)
        json.dump(data, f_w, indent=4, ensure_ascii=False)


class Notifier(metaclass=abc.ABCMeta):
    def __init__(self):
        self._log_list = []

    def notify(self, address, subject, message):
        self._login()
        self._send(address, subject, message)
        self._logout()
        self._log(address, subject, message)
        # // войти в систему доставки сообщений

    @abc.abstractmethod
    def _login(self):
        pass

    # // отправка сообщения
    @abc.abstractmethod
    def _send(self, address, subject, message):
        pass

    # // выход
    @abc.abstractmethod
    def _logout(self):
        pass

    # // внутреннее логирование, задаем поведение по умолчанию
    def _log(self, address, subject, message):
        self._log_list.append([address, subject, message])


class EmailNotifier(Notifier):  # имитация информирования по email
    def __init__(self):
        super().__init__()
        self.mail_from = ''

    def _login(self):
        # // no need to login
        pass

    def _send(self, mail_to, subject, message):
        print(f'send_mail: {mail_to}, {subject}, {message}')

    def _logout(self):
        # // no need to logout
        pass


class SmsNotifier(Notifier):  # имитация информирования по смс
    def __init__(self):
        super().__init__()
        self.mail_from = ''

    def _login(self):
        # // no need to login
        pass

    def _send(self, sms_to, subject, message):
        print(f'send_sms: {sms_to}, {subject}, {message}')

    def _logout(self):
        # // no need to logout
        pass


class NotifierFabric:
    @staticmethod
    def get_notifier(communication_type):
        if communication_type == 'EMAIL':
            return EmailNotifier()
        elif communication_type == 'SMS':
            return SmsNotifier()
