from django.contrib import admin
from .models import (
   BlogPost,
)

# Enregistrement des modèles dans l'interface d'administration avec des filtres
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
