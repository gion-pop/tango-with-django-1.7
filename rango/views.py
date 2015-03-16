from django.shortcuts import render
from django.http import HttpResponse


def index(req):
    return HttpResponse('Rango says hey there world!')
