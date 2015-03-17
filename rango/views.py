from django.shortcuts import render
from django.http import HttpResponse


def index(req):
    ctx_dict = {'boldmessage': 'I am bold font from the context'}
    return render(req, 'rango/index.html', ctx_dict)


def about(req):
    return render(req, 'rango/about.html')
