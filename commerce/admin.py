from django.contrib import admin
from .models import (
    Category, Product, UserProfile, Order, Cart, CartItem, OrderItem
)

# Enregistrement des modèles dans l'interface d'administration avec des filtres

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number')
    search_fields = ('user__username', 'address', 'phone_number')

class OrderItemInline(admin.TabularInline):  # ou admin.StackedInline
    model = OrderItem
    extra = 1  # Nombre de lignes vides affichées pour ajouter de nouveaux articles

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'order_date', 'total_price']
    list_filter = ['status', 'order_date']
    search_fields = ['user__username', 'id']
    inlines = [OrderItemInline]  # Ajouter les articles de la commande

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Montant total'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    search_fields = ('cart__user__username', 'product__name')
    list_filter = ('cart__user', 'product__category')

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Prix total'