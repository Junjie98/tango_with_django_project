from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

#register both category and page class to admin interface
admin.site.register(Category)
admin.site.register(Page, PageAdmin)

