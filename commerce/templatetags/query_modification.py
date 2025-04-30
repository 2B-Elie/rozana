from django import template
from urllib.parse import urlencode
from django.http import QueryDict

register = template.Library()

@register.simple_tag(takes_context=True)
def modify_query(context, **kwargs):
    request = context['request']
    query_dict = request.GET.copy()
    
    for key, value in kwargs.items():
        if value is None:
            query_dict.pop(key, None)
        else:
            query_dict[key] = value
    
    # Gestion spéciale pour les catégories (multiples valeurs)
    if 'category' in kwargs and kwargs['category'] is None:
        query_dict.pop('category', None)
    
    return query_dict.urlencode()