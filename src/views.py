from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render_to_response



def hello(request,age):
    try:
        age = int(age)
    except: 
        raise Http404
    t = Template('my name os {{ name.upper }}, and i {{ year }} old')
    for name in ('amir','aki','asd'):
        a = t.render(Context({ 'name': name,'year': age }))
    return HttpResponse(a)



def error404(request):
    return HttpResponse('Error 404 Not Found !')


def current_datetime(request):
    now = datetime.now()
    return render_to_response('myTemplate.html', {'current_date': now})