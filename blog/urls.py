from django.urls import path
from .views import BlogView, BlogSingleView

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('<int:pk>/', BlogSingleView.as_view(), name='blog_single'),
]