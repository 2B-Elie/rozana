from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from rozana.models import ContactInfo
from .models import BlogPost, Comment
from commerce.models import Cart
from .forms import CommentForm  # Créez ce formulaire si nécessaire
from django.contrib.auth.mixins import LoginRequiredMixin

class BlogView(ListView):
    model = BlogPost
    template_name = 'pages/blog.html'
    context_object_name = 'blog_posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request  # Important pour le template tag
        context['contact_info'] = ContactInfo.objects.first()
        context['categories'] = dict(BlogPost.CATEGORY_CHOICES)
        context['recent_posts'] = BlogPost.objects.all().order_by('-created_at')[:5]
        
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = cart.items.all()
            context['cart_total'] = cart.total_price()
        else:
            context['cart_items'] = []
            context['cart_total'] = 0
        
        return context
    
class BlogSingleView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'pages/blog_single.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(BlogPost.CATEGORY_CHOICES)
        context['recent_posts'] = BlogPost.objects.exclude(id=self.object.id).order_by('-created_at')[:5]
        context['related_posts'] = BlogPost.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:2]
        context['comments'] = self.object.post_comments.select_related('author').all()
        context['form'] = CommentForm()
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user  # Assurez-vous que l'auteur est bien défini
            comment.save()
            return redirect('blog_single', pk=self.object.pk)
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)