from wsgiref.simple_server import make_server
from main_app.main import FrameworkAPI
from urls import routes, fronts


app = FrameworkAPI(routes, fronts)


with make_server('', 8080, app) as httpd:
    print("RUN port 8080...")
    httpd.serve_forever()
