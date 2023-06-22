import json
from webob import Request, Response
from urllib.parse import unquote_plus


class API:
    def __init__(self):
        self.routes = {}

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

        if method == 'GET':
            query_string = environ['QUERY_STRING']
            request_params = self.parse_input_data(query_string)
            print(request_params)  # выводим GET параметры в консоль
            if request_params != {}:  # сохранение данных в файл
                with open('data.json', 'r', encoding='utf-8') as f_r:
                    data = json.load(f_r)

                with open('data.json', 'w', encoding='utf-8') as f_w:
                    order = data['get']
                    order.append(request_params)
                    json.dump(data, f_w, indent=4, ensure_ascii=False)

        if method == 'POST':
            content_length_data = environ['CONTENT_LENGTH']
            content_length = int(content_length_data) if content_length_data else 0
            data = environ['wsgi.input'].read(content_length) \
                if content_length > 0 else b''
            data = data.decode(encoding='utf-8')
            request_params = self.parse_input_data(unquote_plus(data))
            print(request_params)  # выводим POST параметры в консоль
            if request_params != {}:  # сохранение данных в файл
                with open('data.json', 'r', encoding='utf-8') as f_r:
                    data = json.load(f_r)

                with open('data.json', 'w', encoding='utf-8') as f_w:
                    order = data['post']
                    order.append(request_params)
                    json.dump(data, f_w, indent=4, ensure_ascii=False)
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response
        self.response_404(response)
        return response

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
