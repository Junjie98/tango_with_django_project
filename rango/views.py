from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    html = "<a href='/rango/about/'>About</a>"
    return HttpResponse("Rango says hey there partner!" + html)

def about(request):
    html = "<a href='/rango/'>Index</a>"
    return HttpResponse("Rango says here is the about page." + html)

