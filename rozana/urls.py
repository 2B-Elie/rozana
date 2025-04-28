"""
URL configuration for rozana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView, AboutPageView, ContactPageView


urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # ← important
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS

    #urls for home pages
    path('', HomePageView.as_view(), name='home'),

    #urls for blog
    path('blog/', include('blog.urls')),

    #urls for commerce
    path('commerce/', include('commerce.urls')),

    #urls for conditions
    path('conditions/', include('conditions.urls')),

    # #urls for account
    # path('account/', include('account.urls')),

    # #urls for search
    # path('search/', include('search.urls')),

    # #urls for contact
    # path('contact/', include('contact.urls')),

    #urls for about us
    path('about-us/',AboutPageView.as_view(), name='about'),

    #urls for contact
    path('contact/',ContactPageView.as_view(), name='contact'),

    # #urls for terms and conditions
    # path('terms-and-conditions/', include('terms_and_conditions.urls')),

    # #urls for privacy policy
    # path('privacy-policy/', include('privacy_policy.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#Modify Site Header
admin.site.site_header = 'Rozana Healthy Cosmetics'
#Modify Site Title
admin.site.site_title = 'Rozana Healthy Cosmetics'
#Modify Site Index Title
admin.site.index_title = 'Rozana Healthy Cosmetics Administration'