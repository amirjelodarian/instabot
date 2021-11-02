from django.http import HttpResponse
from django.http.response import Http404
def hello(request,age):
    try:
        age = int(age)
    except: 
        raise Http404
    a = 'amir'
    html = "<html><body><h1> %s , i am %s year old</h1></body></html>" %(a,age)
    return HttpResponse(html)
def error404(request):
    return HttpResponse('Error 404 Not Found !')