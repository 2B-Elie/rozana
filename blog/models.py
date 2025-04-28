from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class BlogPost(models.Model):
    # Options pour les catégories
    CATEGORY_CHOICES = [
        ('skincare', 'Soins de la peau'),
        ('makeup', 'Maquillage'),
        ('fragrance', 'Parfums'),
        ('haircare', 'Soins capillaires'),
        ('natural', 'Produits naturels'),
        ('tips', 'Conseils beauté'),
        ('trends', 'Tendances cosmétiques'),
        ('reviews', 'Avis produits'),
    ]

    title = models.CharField(max_length=255)
    content = CKEditor5Field()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='skincare')  # Nouveau champ

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"

from django.contrib.auth.models import User
class Comment(models.Model):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='post_comments')  # Changé ici
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"