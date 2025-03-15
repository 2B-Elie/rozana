from django.urls import path
from .views import CustomLoginView, UserRegisterView, ProfileView, ProductListView, ProductDetailView, checkout,add_to_cart, update_cart ,CartView,RemoveFromCartView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  



    path('', ProductListView.as_view(), name='shop'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'), 
    path('cart/', CartView.as_view(), name='cart'),
    path('remove-from-cart/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'),
]
