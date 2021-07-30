from django.shortcuts import render,redirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.urls import reverse

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
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html')


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


def add_category(request):
    form = CategoryForm() #this line return the view for Add a Category page.

    #a http post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #did the user submit data via the form?
        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return redirect('/rango/')
        else:
            print(form.errors)
    #handle good,bad or no form supplied cases.
    #render the form with error messages if there is any.
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            #reverse() looks up URL names in our urls.py modules.
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category} 
    return render(request, 'rango/add_page.html', context=context_dict)