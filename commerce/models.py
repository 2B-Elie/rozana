from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

# Modèle pour les utilisateurs (utilisation du modèle intégré de Django)
# Vous pouvez étendre le modèle utilisateur de Django si vous avez besoin de champs supplémentaires
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True) 
    last_name = models.CharField(max_length=100, null=True, blank=True)   
    delivery_address = models.CharField(max_length=255, null=True, blank=True) 

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Profils des utilisateurs"
        verbose_name_plural = "Profils des utilisateurs"



# # Signaux pour créer automatiquement un profil utilisateur lorsque l'utilisateur est créé
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1.2. Boutique
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Catégories"
        verbose_name_plural = "Catégories"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Ajouter ce champ

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produits"
        verbose_name_plural = "Produits"
        ordering = ['id']    

    
# Modèle pour les commandes
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'En attente'),
        ('shipped', 'Expédié'),
        ('delivered', 'Livré'),
        ('cancelled', 'Annulé'),
    ])

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    def total_price(self):
        """
        Calcule le montant total de la commande en fonction des articles associés.
        """
        return sum(item.product.price * item.quantity for item in self.items.all())    

    class Meta:
        verbose_name = "Commandes"
        verbose_name_plural = "Commandes"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"        


# Modèle pour le panier
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Panier de {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    class Meta:
        verbose_name = "Paniers"
        verbose_name_plural = "Paniers"


# Modèle pour les articles du panier
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} dans le panier de {self.cart.user.username}"

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Articles du panier"
        verbose_name_plural = "Articles du panier"


# Signaux pour créer automatiquement un panier lorsque l'utilisateur est créé
@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    if hasattr(instance, 'cart'):
        instance.cart.save()