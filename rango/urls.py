from django.urls import path
from rango import views

app_name = 'rango'
#the first parameter is the string to match in path.
#the second parameter tells Django what view to call if the pattern '' is matched.
#third parameter is optional called name. Convinient way to reference the view. & by naming our URL mapping
#we can employ reverse URL matching. This is we can reference the URL mapping by name rather than by the URL.
urlpatterns = [ 
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page')
]