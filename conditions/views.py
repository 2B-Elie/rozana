from django.shortcuts import render
from django.views.generic import TemplateView
from rozana.models import ContactInfo

# Create your views here.


class FAQPageView(TemplateView):
    template_name = 'pages/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        return context
    


class PolitiqueRetourView(TemplateView):
    template_name = 'pages/politique_retour.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        return context
class ConditionGeneralView(TemplateView):
    template_name = 'pages/conditions_generale.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        return context       