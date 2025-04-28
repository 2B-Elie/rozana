from django import template
from urllib.parse import urlencode
from django.http import QueryDict

register = template.Library()

@register.simple_tag(takes_context=True)
def modify_query(context, **kwargs):
    """
    Modifie les paramètres de requête existants
    Usage: ?{% modify_query page=1 category=None %}
    """
    request = context['request']
    query_dict = request.GET.copy()
    
    for key, value in kwargs.items():
        if value is None:
            query_dict.pop(key, None)
        else:
            query_dict[key] = value
    
    return query_dict.urlencode()

from django.db.models import Count
from ..models import BlogPost  # Adaptez l'import selon votre structure

@register.filter
def get_item(dictionary, key):  
    return dictionary.get(str(key), '')

@register.filter
def post_count(category_value):
    return BlogPost.objects.filter(category=category_value).count()

