from django.shortcuts import render
from django.http import HttpResponse


def index(req):
    return HttpResponse('Rango says hey there world!<br><a href="/rango/about">About page</a>')


def about(req):
    return HttpResponse('Rango says here is the about page.<br><a href="/rango">Top page</a>')
