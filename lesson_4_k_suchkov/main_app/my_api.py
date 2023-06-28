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

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)
        method = environ['REQUEST_METHOD']

        print(f"method {method}")

        if method == 'GET':  # например, http://127.0.0.1:8080/?utils=1&test=ok
            query_string = environ['QUERY_STRING']
            request_params = self.parse_input_data(query_string)
            print(request_params)  # выводим GET параметры в консоль
            if request_params != {}:
                save_data(request_params, "GET")  # сохранение данных в файл в раздел GET

        if method == 'POST':
            content_length_data = environ['CONTENT_LENGTH']
            content_length = int(content_length_data) if content_length_data else 0
            data = environ['wsgi.input'].read(content_length) \
                if content_length > 0 else b''
            data = data.decode(encoding='utf-8')

            request_params = self.parse_input_data(unquote_plus(data))

            print(request_params)  # выводим POST параметры в консоль

            if 'solid' in request_params:  # если запрос solid, то меняем переменную для отображения на сайте
                self.solid = self.get_solid(request_params)

            if request_params != {} and 'solid' not in request_params:
                save_data(request_params, "POST")  # сохранение данных в файл в раздел POST

            if 'create_user' in request_params:
                kind = request_params['your_type']
                name = request_params['your_name']
                self.main.add_user(kind, name)

            if 'create_group' in request_params:
                kind = request_params['your_type']
                data = request_params['group_data']
                self.main.add_group(kind, data)

            if 'copy_group' in request_params:
                group = request_params['group_to']
                for el in self.main.groups:
                    if el.name == group:
                        group = el.copy_group()  # для копирования применяется метод из GroupPrototype
                        self.main.groups.append(group)

        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response
        self.response_404(response)
        return response

    def get_solid(self, request_params):
        try:
            self.solid = SOLID[int(request_params['solid'])]
            return self.solid
        except:
            pass

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
