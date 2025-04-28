from django_ckeditor_5.fields import CKEditor5Field
from django.db import models

from django.db import models

class HomePage(models.Model):
    slogan = models.CharField(max_length=255, help_text="Court texte décrivant la mission ou les valeurs de l’entreprise.")
    promo_video = models.FileField(upload_to='home_videos/', null=True, blank=True, help_text="Vidéo promotionnelle (si disponible).")

    def __str__(self):
        return self.slogan

    class Meta:
        verbose_name = "Page d'accueil"
        verbose_name_plural = "Pages d'accueil"

class HomePageImage(models.Model):
    home_page = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='home_images/', help_text="Images supplémentaires pour la page d'accueil.")

    def __str__(self):
        return f"Image de {self.home_page}"


    
class FeaturedProduct(models.Model):
    home_page = models.ForeignKey(HomePage, related_name='featured_products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = CKEditor5Field()
    image = models.ImageField(upload_to='featured_products/')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Produit phare"
        verbose_name_plural = "Produit phare"

    
class ReturnPolicy(models.Model):
    policy_text = CKEditor5Field(help_text="Politique de retour et d’échange.")

    class Meta:
        verbose_name = "Politique de retour"
        verbose_name_plural = "Politique de retour"

#  "Qui sommes-nous ?"
class AboutUs(models.Model):
    history = CKEditor5Field(help_text="Texte décrivant la création et les valeurs de Razana Healthy Cosmetics.")
    mission = CKEditor5Field(help_text="Objectifs à long terme et engagement envers les clients.")
    team_photo = models.ImageField(upload_to='team_photos/', null=True, blank=True)

    class Meta:
        verbose_name = "A propos de nous"
        verbose_name_plural = "A propos de nous"

# Page Contact
class ContactInfo(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    tiktok = models.URLField(null=True, blank=True)
    google_maps_location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Info contacts"
        verbose_name_plural = "Info contacts"

# Contenus généraux
class GeneralContent(models.Model):
    logo = models.ImageField(upload_to='logos/', help_text="Logo de l’entreprise en haute résolution.")
    color_palette = CKEditor5Field(help_text="Palette de couleurs et typographie.", null=True, blank=True)
    additional_media = models.FileField(upload_to='media/', null=True, blank=True, help_text="Médias supplémentaires comme icônes spécifiques, bannières publicitaires, etc.")
    
    class Meta:
        verbose_name = "Contenu général"
        verbose_name_plural = "Contenu général"

# Nouveau modèle pour les messages de contact
class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom")
    email = models.EmailField(verbose_name="E-mail")
    subject = models.CharField(max_length=255, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return f"Message de {self.name} - {self.subject}"

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
