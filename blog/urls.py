from django.urls import path
from .views import BlogView, BlogSingleView

urlpatterns = [
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/<int:pk>/', BlogSingleView.as_view(), name='blog_single'),
]