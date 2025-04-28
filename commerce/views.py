from django.shortcuts import render

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, ListView, DetailView, TemplateView, View
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm
from .models import UserProfile, Product, Cart, CartItem, Order, Category, OrderItem

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from rozana.models import ContactInfo


from django.contrib import messages

from .utils import send_whatsapp_message, send_order_email, send_copy_order_email

from django.shortcuts import get_object_or_404, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

class CustomLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'pages/registration/login.html'
    success_url = '/'  # URL par défaut après la connexion

    def form_valid(self, form):
        # Connecte l'utilisateur
        auth_login(self.request, form.get_user())

        # Récupère l'utilisateur connecté
        user = self.request.user

        # Vérifie si l'utilisateur a un profil
        if hasattr(user, 'userprofile'):
            profile = user.userprofile

            # Vérifie si les champs requis sont remplis
            if profile.first_name and profile.last_name and profile.delivery_address:
                return redirect('home')  # Redirige vers la page d'accueil
            else:
                messages.info(self.request, 'Veuillez compléter votre profil.')
                return redirect('profile')  # Redirige vers la page de profil
        else:
            # Si l'utilisateur n'a pas de profil, redirige vers la page de profil
            messages.info(self.request, 'Veuillez créer votre profil.')
            return redirect('profile')

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'pages/registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Sauvegarde l'utilisateur
        user = form.save()

        # Crée le profil utilisateur avec les données supplémentaires
        UserProfile.objects.create(
            user=user,
            address=form.cleaned_data['address'],
            phone_number=form.cleaned_data['phone_number']
        )

        return super().form_valid(form)
    

class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'pages/registration/profile.html'
    success_url = reverse_lazy('profile')
    

    def get_object(self):
        return self.request.user.userprofile
    

    def form_valid(self, form):
        # Ajoute un message de succès
        messages.success(self.request, 'Votre profil a été mis à jour avec succès.')
        return super().form_valid(form)
    


from django.http import QueryDict

def product_list(request):
    # Récupérer les catégories sélectionnées
    selected_categories = request.GET.getlist('category', [])
    
    # Filtrer les produits
    if selected_categories:
        product_list = Product.objects.filter(category_id__in=selected_categories).order_by('name')
    else:
        product_list = Product.objects.all().order_by('name')
    
    # Pagination
    paginator = Paginator(product_list, 9)  # 9 produits par page
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    # Contexte pour le template
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'selected_categories': selected_categories,
        'contact_info': ContactInfo.objects.first(),
    }
    
    # Ajouter les informations du panier si l'utilisateur est authentifié
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        context['cart_items'] = cart.items.all()
        context['cart_total'] = cart.total_price()
    else:
        context['cart_items'] = []
        context['cart_total'] = 0
    
    return render(request, 'pages/shop/product_grid.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Ajouter les catégories au contexte
        context['contact_info'] = ContactInfo.objects.first()
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = cart.items.all()
            context['cart_total'] = cart.total_price()
        else:
            context['cart_items'] = []
            context['cart_total'] = 0        
        return context

from django.core.exceptions import ValidationError

def checkout(request):
    if request.method == 'POST':
        try:
            user = request.user
            cart = Cart.objects.get(user=user)

            # Créer une commande principale
            order = Order.objects.create(user=user, status='pending')

            # Ajouter chaque article du panier à la commande
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            # Calculer le montant total de la commande
            total_price = order.total_price()

            # Vider le panier
            cart.items.all().delete()

            # Récupérer le profil utilisateur
            profile = UserProfile.objects.get(user=user)

            # Construire le nom complet, avec fallback sur le username
            full_name = f"{profile.first_name or ''} {profile.last_name or ''}".strip()
            if not full_name:
                full_name = user.username

            # Préparer le message WhatsApp
            whatsapp_message = f"Nouvelle commande #{order.id} de {full_name}\n\n"
            whatsapp_message += "📦 Détails de la commande :\n"

            for item in order.items.all():
                whatsapp_message += f"- {item.product.name} : {item.quantity} x {item.product.price} XOF\n"

            whatsapp_message += f"\n💰 Montant total : {total_price} XOF\n"
            whatsapp_message += f"\n📍 Adresse de livraison : {profile.delivery_address or 'Non spécifiée'}\n"
            whatsapp_message += f"📞 Contact : {profile.phone_number or 'Non spécifié'}\n"
            # Message à envoyer au client
            copy_message = f"Bonjour {full_name},\n\n"
            copy_message += f"Merci pour votre commande #{order.id} sur notre boutique !\n\n"
            copy_message += "🧾 Détails de la commande :\n"

            for item in order.items.all():
                copy_message += f"- {item.product.name} : {item.quantity} x {item.product.price} XOF\n"

            copy_message += f"\n💰 Montant total : {total_price} XOF\n"
            copy_message += f"\n📍 Adresse de livraison : {profile.delivery_address or 'Non spécifiée'}\n"
            copy_message += f"📞 Contact : {profile.phone_number or 'Non spécifié'}\n"
            copy_message += "\nNous vous contacterons bientôt pour la confirmation.\n\nMerci de votre confiance !"

            # Envoyer la copie par email au client
            subject = f"Confirmation de votre commande #{order.id}"
            send_copy_order_email(subject, copy_message, user.email)

            # Envoyer une notification WhatsApp
            #send_whatsapp_message(whatsapp_message)

            # Envoyer un e-mail
            email_subject = f"Nouvelle commande #{order.id}"
            email_message = f"Une nouvelle commande a été passée par {user.username}.\n\nDétails :\n\n{whatsapp_message}"
            send_order_email(email_subject, email_message)

            # Message de succès
            messages.success(request, 'Votre commande a été passée avec succès !')
            return redirect('home')

        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {str(e)}")
            return redirect('cart')

    return render(request, 'pages/shop/checkout.html')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Vérifiez si l'utilisateur a un panier
    cart, created = Cart.objects.get_or_create(user=user)

    # Vérifiez si le produit est déjà dans le panier
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1  # Augmentez la quantité si le produit est déjà dans le panier
        cart_item.save()

    messages.success(request, f"{product.name} a été ajouté à votre panier.")
    return redirect('shop')  # Redirigez vers la page de la boutique ou du panier


class CartView(TemplateView):
    template_name = 'pages/shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(user=self.request.user)
            context['cart_items'] = cart.items.all()
            context['cart_total'] = cart.total_price()
        else:
            context['cart_items'] = []
            context['cart_total'] = 0
        return context


class RemoveFromCartView(View):
    def get(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return redirect('cart')        
    
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "La quantité a été mise à jour.")
        else:
            cart_item.delete()
            messages.success(request, "L'article a été supprimé du panier.")
        
        return redirect('cart')
