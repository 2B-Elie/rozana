from django.views.generic import ListView, DetailView
from rozana.models import ContactInfo
from .models import BlogPost
from commerce.models import Cart


class BlogView(ListView):
    model = BlogPost
    template_name = 'pages/blog.html'
    context_object_name = 'blog_posts'
    paginate_by = 6

    def get_queryset(self):
        # Filtrer par catégorie si un paramètre est passé dans l'URL
        category = self.request.GET.get('category')
        if category:
            return BlogPost.objects.filter(category=category)
        return BlogPost.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        context['categories'] = dict(BlogPost.CATEGORY_CHOICES)  # Ajouter les catégories au contexte

        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = cart.items.all()
            context['cart_total'] = cart.total_price()
        else:
            context['cart_items'] = []
            context['cart_total'] = 0        
        return context

class BlogSingleView(DetailView):
    model = BlogPost  # Modèle à utiliser
    template_name = 'pages/blog_single.html'  # Template à utiliser
    context_object_name = 'post'  # Nom de la variable dans le template

    def get_context_data(self, **kwargs):
        # Ajouter des données supplémentaires au contexte
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()  # Informations de contact
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = cart.items.all()
            context['cart_total'] = cart.total_price()
        else:
            context['cart_items'] = []
            context['cart_total'] = 0        
        return context    