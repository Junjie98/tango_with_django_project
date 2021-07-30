from django.shortcuts import render,redirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    #construct a dictionary to pass to the template engine as its context.
    #note the key boldmessage matches to {{ boldmessage }} in the template
    category_list = Category.objects.order_by('-likes')[:5] #to retrieve the top 5 categories in des order!
    page_list = Page.objects.order_by('-views')[:5]# again. Same as above
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    #return a rendered response to send to the client.
    #we make use of the shortcut function to make our lives easier
    #note that the first parameter is the template we wish to use.
    response = render(request, 'rango/index.html', context=context_dict)

    #return response back to user. Update any cookies that requries changed.
    return response

def about(request):
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

@login_required #ensure another layer of security? 
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

@login_required #ensure another layer of security? 
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

    
def register(request):
    #boolean value to tell the template if registration
    #was successful or not.
    registered = False

    if request.method == 'POST':
        #an attempt to grab info from the raw form information.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #save user's form data to database
            user = user_form.save()

            #hash the password with set_password method
            #hash it before updating the user object.
            user.set_password(user.password)
            user.save()

            #Now, we sort userprofile instance.
            #since we need to set user attribute ourselves,
            #we set commit=False.
            profile = profile_form.save(commit=False)
            profile.user = user

            #check if user provide a profile pic
            #if he did, get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #save it
            profile.save()

            #update variable to indicate the registration is successful!
            registered = True
        else:
            #specify the issue.
            print(user_form.errors, profile_form.errors)
    else:
        #not a HTTP POST. If that's the case, we render our form using two ModelForm instances.
        user_form = UserForm() #these will be empty blank form, ready for userinput
        profile_form = UserProfileForm()

    #render template depending on the context.
    return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    #pull out the relevant information if it is a POST
    ## We use request.POST.get('<variable>') as opposed
    # to request.POST['<variable>'], because the
    # request.POST.get('<variable>') returns None if the
    # value does not exist, while request.POST['<variable>']
    # will raise a KeyError exception.

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #use Django's machinery to attempt to see if the user/password
        #combination is valid. If valid, a user object is returned.
        user = authenticate(username=username, password=password)

        #if we have the user object then the details are correct.
        #if none, no user with matching credentials was found.
        if user:
            #check if account is still active. (not disabled)
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
                #after login, send user back to the homepage
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            #bad login
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    #Request is not in HTTP POST, display the login form.
    #would most likely be a HTTP GET
    else:    
        return render(request, 'rango/login.html')

            
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

#login_required() decorator to ensure only logged in user can access the view
@login_required
def user_logout(request):
    logout(request)
    #throw them back to the homepage
    return redirect(reverse('rango:index'))


#helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1

        #update last visit cookie now that we have already updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    
    #now, update or set the visit cookie
    request.session['visits'] = visits

    

