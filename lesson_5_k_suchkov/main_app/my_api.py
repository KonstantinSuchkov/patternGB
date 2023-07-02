import time

from webob import Request, Response
from urllib.parse import unquote_plus

from patterns import Kindergarden
from utils import SOLID, save_data


class API:
    def __init__(self):
        self.routes = {}
        self.solid = SOLID[0]  # добавим на страницу another_page принципы solid
        self.main = Kindergarden()  # создание основного класса, отвечающего за контент сайта

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
                self.post_solid(environ)
                response = self.start_page(environ)

            if request_params != {} and 'solid' not in request_params:
                save_data(request_params, "POST")  # сохранение данных в файл в раздел POST

            if 'create_user' in request_params:
                self.post_create_user(request_params)
                response = self.start_page(environ)

            if 'create_group' in request_params:
                self.post_create_group(request_params)
                response = self.start_page(environ)

            if 'copy_group' in request_params:
                self.post_copy_group(request_params)
                response = self.start_page(environ)
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
        self.main.add_user(kind, name)

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
