
from django.contrib import admin
from django.urls import path, include
from .views import FAQPageView, ConditionGeneralView, PolitiqueRetourView

urlpatterns = [
    path('faq', FAQPageView.as_view(), name='faq'),
    path('conditions-generales', ConditionGeneralView.as_view(), name='condition_generale'),
    path('politique-retour', PolitiqueRetourView.as_view(), name='politique_retour'),
]
