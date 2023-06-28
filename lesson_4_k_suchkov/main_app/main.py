class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class FrameworkAPI:
    def __init__(self, routesj, frontsj):
        self.routes = routesj
        self.fronts = frontsj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()
        request = {}
        for front in self.fronts:
            front(request)
        print(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
