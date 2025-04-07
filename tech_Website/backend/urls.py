from django.urls import path
from .views import product_list, product_detail, home, contact_us,cart
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('contact-us/', contact_us, name='contact_us'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('cart/', views.cart, name='cart'),  # Define the 'cart' URL
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
