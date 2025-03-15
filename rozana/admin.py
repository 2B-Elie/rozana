from django.contrib import admin
from .models import (
    FeaturedProduct, HomePage,ReturnPolicy,
    AboutUs, ContactInfo, GeneralContent, HomePageImage, ContactMessage
)

# Enregistrement des modèles dans l'interface d'administration avec des filtres

class HomePageImageInline(admin.TabularInline):
    model = HomePageImage
    extra = 1  # Permet d’ajouter plusieurs images d’un coup

class HomePageAdmin(admin.ModelAdmin):
    list_display = ('slogan', 'get_total_images')  # Affiche le slogan + nombre d'images
    search_fields = ('slogan',)  # Permet de rechercher un HomePage par son slogan
    list_filter = ('slogan',)  # Filtrer par slogan
    inlines = [HomePageImageInline]

    def get_total_images(self, obj):
        return obj.images.count()
    get_total_images.short_description = "Nombre d'images"

class HomePageImageAdmin(admin.ModelAdmin):
    list_display = ('home_page', 'image')  # Affiche la page liée + l’image
    search_fields = ('home_page__slogan',)  # Recherche par slogan de HomePage
    list_filter = ('home_page',)  # Filtrer par HomePage

admin.site.register(HomePage, HomePageAdmin)
admin.site.register(HomePageImage, HomePageImageAdmin)

    
@admin.register(FeaturedProduct)
class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'home_page')
    search_fields = ('name', 'home_page__slogan')
    list_filter = ('home_page',)

@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_text',)
    search_fields = ('policy_text',)

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('history', 'mission')
    search_fields = ('history', 'mission')

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_number', 'email')
    search_fields = ('address', 'phone_number', 'email')

@admin.register(GeneralContent)
class GeneralContentAdmin(admin.ModelAdmin):
    list_display = ('logo', 'color_palette')
    search_fields = ('color_palette',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    ordering = ('-created_at',)  # Tri par date de création (du plus récent au plus ancien)
