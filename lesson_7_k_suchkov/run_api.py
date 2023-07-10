from wsgiref.simple_server import make_server

from db_start import start_bd
from main_app.my_api import API, FakeApp
from main_app.templator import render
from datetime import date

from urls import test_time, weather


# инициализация базы данных
start_bd()

# запуск основного кода
app = API()
# app = FakeApp()

# наполнение тестовыми данными
app.main.create_test_data()


@app.route("/")
@app.debug
def home(request, response):
    response.text = render('index.html',
                           date=str(date.today()),
                           time=str(test_time()),
                           weather=str(weather()),
                           )


@app.route("/examples")
@app.debug
def examples(request, response):
    response.text = render('examples.html', main=app.main, user_bd=app.user_bd)


@app.route("/contact")
@app.debug
def contact(request, response):
    response.text = render('contact.html')


@app.route("/page")
@app.debug
def page(request, response):
    response.text = render('page.html')


@app.route("/another_page")
@app.debug
def another_page(request, response):
    response.text = render('another_page.html', solid=app.solid)


@app.route("/create_user")
@app.debug
def create_user(request, response):
    response.text = render('create_user.html', main=app.main)


@app.route("/user_detail")
@app.debug
def user_detail(request, response):
    user = request.environ
    try:
        user = user['current_user']
        id = user['user_id']
        response.text = render('user_detail.html',
                               main=app.main,
                               current_user=user,
                               user_bd=app.user_bd.find_by_id(id),
                               user_main=app.user_bd
                               )
    except:
        response.text = render('user_detail.html', main=app.main, current_user=user, user_bd=app.user_bd)


@app.route("/create_group")
@app.debug
def create_group(request, response):
    response.text = render('create_group.html', main=app.main)


with make_server('', 8080, app) as httpd:
    print("RUN port 8080...")
    httpd.serve_forever()
