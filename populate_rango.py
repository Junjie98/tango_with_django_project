import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup() #this is to import my Django project's setting
from rango.models import Category, Page

def populate():
    #first, create a lists of dictionary containing the pages
    #we want to add into each category
    #then we will create a dictionary of dictionaries for our categories
    #this may seem a confusing, but it allows us to iterate
    #thru each data structure, and add the data to our models.
    python_pages = [{'title': 'Official Python Tutorial', 'url':'http://docs.python.org/3/tutorial/'},
    {'title':'How to Think like a Computer Scientist', 'url':'http://www.greenteapress.com/thinkpython/'},
    {'title':'Learn Python in 10 Minutes', 'url':'http://www.korokithakis.net/tutorials/python/'} ]

    django_pages = [{'title':'Official Django Tutorial',
 'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
 {'title':'Django Rocks', 'url':'http://www.djangorocks.com/'},
 {'title':'How to Tango with Django', 'url':'http://www.tangowithdjango.com/'}]

    other_pages = [{'title':'Bottle', 'url':'http://bottlepy.org/docs/dev/'},
    {'title':'Flask', 'url':'http://flask.pocoo.org'} ]

    cats = {'Python': {'pages': python_pages},
    'Django': {'pages': django_pages},
    'Other Frameworks': {'pages': other_pages} }

    #this code below goes through the cats dictionary then adds each category,
    #and then adds all the associated pages for that category.

    for cat, cat_data in cats.items():
        c = add_cat(cat) #bacause page req category ref.
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    #printout the categories we have added so far.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

#main method here *For my own referrence*
#Code within a conditional if __name__ == '__main__' statement will therefore
#only be executed when the module is run as a standalone Python script.
#Importing the module will not run this code; any classes or functions will
#however be fully accessible to you.

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()

    