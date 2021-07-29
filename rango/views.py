from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    #construct a dictionary to pass to the template engine as its context.
    #note the key boldmessage matches to {{ boldmessage }} in the template
    category_list = Category.objects.order_by('-likes')[:5] #to retrieve the top 5 categories in des order!
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    #return a rendered response to send to the client.
    #we make use of the shortcut function to make our lives easier
    #note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #html = "<a href='/rango/'>Index</a>" 
    #return HttpResponse("Rango says here is the about page." + html)
    context_dict = {'boldmessage': 'This tutorial has been put together by Junjie Low'}
    return render(request, 'rango/about.html', context=context_dict)
