from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    #construct a dictionary to pass to the template engine as its context.
    #note the key boldmessage matches to {{ boldmessage }} in the template
    category_list = Category.objects.order_by('-likes')[:5] #to retrieve the top 5 categories in des order!
    page_list = Page.objects.order_by('-views')[:5]# again. Same as above
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    #return a rendered response to send to the client.
    #we make use of the shortcut function to make our lives easier
    #note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #html = "<a href='/rango/'>Index</a>" 
    #return HttpResponse("Rango says here is the about page." + html)
    context_dict = {'boldmessage': 'This tutorial has been put together by Junjie Low'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:#these comments are for my own referrences. So it is easier to remember what's going on.
        #can we find a category name slug with the given name?
        #if we cant, the .get() method raises a doesnotexist exception
        #.get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        #retrive all associated pages
        #the filter() will retrun a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        #adds our results to the template context under name pages.
        context_dict['pages'] = pages
        #we also add the category object from the database to the context dictionary.
        #we will use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        #catch the error & do nothing.
        #the template will display 'no category' message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    #render response and return to client.
    return render(request, 'rango/category.html', context=context_dict)

