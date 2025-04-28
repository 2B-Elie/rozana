from django.contrib import admin
from .models import (
   BlogPost,Comment
)

# Enregistrement des modèles dans l'interface d'administration avec des filtres
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    raw_id_fields = ('post',)
    autocomplete_fields = ('post',)