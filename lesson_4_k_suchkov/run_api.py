from wsgiref.simple_server import make_server
from main_app.my_api import API
from main_app.templator import render
from datetime import date

from urls import test_time, weather

# запуск основного кода
app = API()
# добавление тестовых групп
app.main.add_group('fullday', 'Ягодки')
app.main.add_group('start', 'Ромашка')

@app.route("/")
def home(request, response):
    response.text = render('index.html',
                           date=str(date.today()),
                           time=str(test_time()),
                           weather=str(weather()),
                           )


@app.route("/examples")
def examples(request, response):
    response.text = render('examples.html', main=app.main)


@app.route("/contact")
def contact(request, response):
    response.text = render('contact.html')


@app.route("/page")
def page(request, response):
    response.text = render('page.html')


@app.route("/another_page")
def another_page(request, response):
    response.text = render('another_page.html', solid=app.solid)


@app.route("/create_user")
def create_user(request, response):
    response.text = render('create_user.html', main=app.main)


@app.route("/create_group")
def create_group(request, response):
    response.text = render('create_group.html', main=app.main)

with make_server('', 8080, app) as httpd:
    print("RUN port 8080...")
    httpd.serve_forever()
