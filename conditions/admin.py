from django.contrib import admin
from .models import (
 FAQ, TermsAndConditions
)

# Enregistrement des modèles dans l'interface d'administration avec des filtres

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question', 'answer')

@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('content',)
    search_fields = ('content',)

