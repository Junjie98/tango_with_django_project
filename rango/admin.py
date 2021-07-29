from django.contrib import admin
from rango.models import Category, Page


#register both category and page class to admin interface
admin.site.register(Category)
admin.site.register(Page)

