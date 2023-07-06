from main_app.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html',
                                date=request.get('date', None),
                                time=request.get('time', None),
                                weather=request.get('weather', None)
                                )


class Examples:
    def __call__(self, request):
        return '200 OK', render('examples.html')


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html')


class Page:
    def __call__(self, request):
        return '200 OK', render('page.html')


class Page2:
    def __call__(self, request):
        return '200 OK', render('another_page.html')
