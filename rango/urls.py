from django.urls import path
from rango import views

app_name = 'rango'
#the first parameter is the string to match in path.
#the second parameter tells Django what view to call if the pattern '' is matched.
#third parameter is optional called name. Convinient way to reference the view. & by naming our URL mapping
#we can employ reverse URL matching. This is we can reference the URL mapping by name rather than by the URL.
urlpatterns = [ 
    path('', views.index, name='index'),
    path('about/', views.about, name='about')
]