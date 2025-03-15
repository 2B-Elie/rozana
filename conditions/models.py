from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
#  FAQ
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = RichTextField()

    def __str__(self):
        return self.question
    
      
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"  

# Conditions Générales de Vente (CGV)
class TermsAndConditions(models.Model):
    content = RichTextField(help_text="Texte légal détaillant les politiques de l’entreprise (paiement, livraison, retours, etc.).")

    
    class Meta:
        verbose_name = "Conditions générales"
        verbose_name_plural = "Conditions générales"