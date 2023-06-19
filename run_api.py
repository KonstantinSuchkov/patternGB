from wsgiref.simple_server import make_server
from main_app.my_api import API
from main_app.templator import render
from datetime import date
from urls import test_time, weather


app = API()


@app.route("/index")
def home(request, response):
    response.text = render('index.html',
                           date=str(date.today()),
                           time=str(test_time()),
                           weather=str(weather()),
                           )


@app.route("/examples")
def examples(request, response):
    response.text = render('examples.html')


with make_server('', 8080, app) as httpd:
    print("RUN port 8080...")
    httpd.serve_forever()
