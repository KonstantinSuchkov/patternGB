from datetime import date, datetime
from views import Index, Examples, Contact, Page, Page2
import pytz


def front(request):
    request['date'] = date.today()
    request['time'] = test_time()
    request['weather'] = weather()


def test_time():
    return datetime.now(pytz.timezone('Europe/Moscow'))


def weather():
    import requests
    url = 'https://api.open-meteo.com/v1/forecast?latitude=55.63&longitude=37.32&current_weather=True'
    r = requests.get(url)
    result = r.json()
    current_weather = f'На данный момент в Москве {result["current_weather"]["temperature"]} C.'
    return current_weather


fronts = [front]

routes = {
    '/': Index(),
    '/index/': Index(),
    '/contact/': Contact(),
    '/examples/': Examples(),
    '/page/': Page(),
    '/another_page/': Page2(),
}
