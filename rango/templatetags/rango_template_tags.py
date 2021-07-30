from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):#this method returns a dictionary. (onekey/value pairing)
    return {'categories': Category.objects.all(),
    'current_category': current_category}