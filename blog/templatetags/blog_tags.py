from django import template
from ..models import BlogPost, Comment

register = template.Library()

@register.filter
def post_count(category_value):
    return BlogPost.objects.filter(category=category_value).count()

@register.simple_tag
def total_posts():
    return BlogPost.objects.count()