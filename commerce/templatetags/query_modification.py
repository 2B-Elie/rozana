from django import template

register = template.Library()

@register.simple_tag
def modify_query(**kwargs):
    # Cette fonction permet de modifier ou ajouter des paramètres à la query string
    from django.http import QueryDict
    from urllib.parse import urlencode
    
    request = kwargs.pop('request', None)
    if request is None:
        return ''
    
    query_dict = request.GET.copy()
    
    for key, value in kwargs.items():
        if value is None:
            if key in query_dict:
                del query_dict[key]
        else:
            query_dict[key] = value
    
    # Gestion spéciale pour les catégories (multiples valeurs)
    if 'category' in kwargs:
        if kwargs['category'] is None:
            query_dict.pop('category', None)
        else:
            query_dict.setlist('category', [str(kwargs['category'])])
    
    return query_dict.urlencode()

