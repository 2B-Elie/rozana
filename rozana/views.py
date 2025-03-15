from django.views.generic import TemplateView
from .models import HomePage, HomePageImage, FeaturedProduct, ContactInfo
from commerce.models import Category, Cart, Product
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import ContactForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homepage = HomePage.objects.first()
        context['homepage'] = homepage
        context['contact_info'] = ContactInfo.objects.first()
        context['featured_products'] = FeaturedProduct.objects.filter(home_page=homepage)
        context['carousel_images'] = HomePageImage.objects.filter(home_page=homepage) if homepage else []
        context['categories'] = Category.objects.all()  # Ajouter les catégories au contexte

                # Ajouter les 8 derniers produits
        context['latest_products'] = Product.objects.order_by('-created_at')[:8]

        # Ajouter les articles du panier de l'utilisateur connecté
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = cart.items.all()
            context['cart_total'] = cart.total_price()
        else:
            context['cart_items'] = []
            context['cart_total'] = 0
        return context


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()

        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = cart.items.all()
            context['cart_total'] = cart.total_price()
        else:
            context['cart_items'] = []
            context['cart_total'] = 0
        return context
    

class ContactPageView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Votre message a bien été envoyé. Nous vous répondrons bientôt !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = cart.items.all()
            context['cart_total'] = cart.total_price()
        else:
            context['cart_items'] = []
            context['cart_total'] = 0

        return context
