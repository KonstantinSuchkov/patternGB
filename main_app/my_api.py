import sqlite3
import time

from webob import Request, Response
from urllib.parse import unquote_plus

from arch_patterns import UnitOfWork, UserMapper, UserFactory
from patterns import Kindergarden
from utils import SOLID, save_data, NotifierFabric


class API:
    def __init__(self):
        self.routes = {}
        self.solid = SOLID[0]  # добавим на страницу another_page принципы solid
        self.main = Kindergarden()  # создание основного класса, отвечающего за контент сайта

        self.postman_sms = NotifierFabric.get_notifier('SMS')  # создание оповещения Шаблонный метод
        self.postman_email = NotifierFabric.get_notifier('EMAIL')  # (поведенческий паттерн)

        connection = sqlite3.connect('main_db.sqlite')
        UnitOfWork.new_current()
        self.user_bd = UserMapper(connection)

    def route(self, path):

        def wrapper(handler):
            self.routes[path] = handler
            self.routes[f'{path}/'] = handler
            return handler
        return wrapper

    @staticmethod
    def debug(function):

        def wrapped(*args):
            start_time = time.perf_counter_ns()
            res = function(*args)
            print(f'--- Function {function.__name__}, time completed: ', time.perf_counter_ns() - start_time)
            return res

        return wrapped

    def __call__(self, environ, start_response):
        response = self.start_page(environ)

        method = environ['REQUEST_METHOD']
        request_params = None
        if method == 'GET':  # например, http://127.0.0.1:8080/?utils=1&test=ok
            request_params = self.method_get(environ)

            if request_params != {}:
                self.handler_get(environ, request_params)
                response = self.start_page(environ)

        if method == 'POST':
            request_params = self.method_post(environ)

            if 'solid' in request_params:  # если запрос solid, то меняем переменную для отображения на сайте
                self.post_solid(request_params)

            if request_params != {} and 'solid' not in request_params:
                save_data(request_params, "POST")  # сохранение данных в файл в раздел POST

            if 'create_user' in request_params:
                self.post_create_user(request_params)

            if 'del_user' in request_params:
                self.del_user(request_params)

            if 'create_group' in request_params:
                self.post_create_group(request_params)

            if 'copy_group' in request_params:
                self.post_copy_group(request_params)

            if 'add_pupil' in request_params:
                self.post_add_pupil(request_params)

            if 'del_pupil' in request_params:
                self.post_del_pupil(request_params)

            if 'del_child' in request_params:
                self.del_parenthood(request_params)

            response = self.start_page(environ)  # "обновляем" страницу

        print(f'---> log app ---> method: {method}, params: {request_params}')
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response
        self.response_404(response)
        return response

    def start_page(self, environ):
        request = Request(environ)
        response = self.handle_request(request)
        return response

    @staticmethod
    def handler_get(environ, request_params):
        save_data(request_params, "GET")  # сохранение данных в файл в раздел GET
        environ['current_user'] = request_params

    def post_solid(self, request_params):
        self.solid = self.get_solid(request_params)

    def post_create_user(self, request_params):
        kind = request_params['your_type']
        name = request_params['your_name']
        try:
            new_person = UserFactory.create_user(kind, data=(None, name, kind))
            new_person.mark_new()
            UnitOfWork.get_current().commit()
        except:
            pass
        if kind == 'child':  # если созданный юзер ребенок, то необходимо добавить запись в таблицу parenthood
            new_person = self.user_bd.find_by_name(name)
            parent_id = request_params['your_parent']
            self.user_bd.add_child(new_person, parent_id)

    def del_user(self, request_params):
        id = request_params['user_id']
        try:
            new_person = self.user_bd.find_by_id(id)
            kind = new_person.status
            new_person.mark_removed()
            UnitOfWork.get_current().commit()
            if kind == 'child':
                self.user_bd.delete_parenthood(id)
        except:
            pass

    def del_parenthood(self, request_params):
        row_id = request_params['row_id']
        print('start del parenthood', {row_id})
        self.user_bd.delete_parenthood(row_id)

    def post_create_group(self, request_params):
        kind = request_params['your_type']
        data = request_params['group_data']
        self.main.add_group(kind, data)

    def post_copy_group(self, request_params):
        group = request_params['group_to']
        for el in self.main.groups:
            if el.name == group:
                group = el.copy_group()  # для копирования применяется метод из GroupPrototype
                self.main.groups.append(group)

    def post_add_pupil(self, request_params):
        child_id = request_params['pupil']
        to_group = request_params['to_group']
        child = self.main.get_user(child_id)
        group = self.main.get_group(to_group)
        group.add_pupil(child)

        self.postman_sms.notify('---sms---', group.name, f'У нас новый ученик: {child[3].name}')
        self.postman_email.notify('---email---', group.name, f'У нас новый ученик: {child[3].name}')

    def post_del_pupil(self, request_params):
        child_id = request_params['pupil']
        child = self.main.get_user(child_id)
        group = self.main.check_pupil(child)  # ищем группу где состоит ученик
        try:
            group.del_pupil(child)
            self.postman_sms.notify('---sms---', group.name, f'Группу покинул ученик: {child[3].name}')
            self.postman_email.notify('---email---', group.name, f'Группу покинул ученик: {child[3].name}')
        except:
            pass

    def get_solid(self, request_params):
        try:
            self.solid = SOLID[int(request_params['solid'])]
            return self.solid
        except:
            pass

    def method_get(self, environ):
        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(unquote_plus(query_string))
        return request_params

    def method_post(self, environ):
        content_length_data = environ['CONTENT_LENGTH']
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        data = data.decode(encoding='utf-8')
        request_params = self.parse_input_data(unquote_plus(data))
        return request_params

    @staticmethod
    def response_404(response):
        response.status_code = 404
        response.text = "404 - Not found"

    @staticmethod
    def parse_input_data(data):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result


class FakeApp(API):

    def __init__(self):
        self.app = API()
        super().__init__()

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
