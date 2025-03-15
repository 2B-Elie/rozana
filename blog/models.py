from django.db import models
from ckeditor.fields import RichTextField


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
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='skincare')  # Nouveau champ

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"