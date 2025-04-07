from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Product,CartItem
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



# API View to list all products
class ProductListAPI(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# API View to get product details
class ProductDetailAPI(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def home(request):
    # Get the best products (can include discounted and non-discounted products)
    best_products = Product.objects.all().order_by('-rating')[:5]  # Example: top 5 rated products

    # Get the discounted products
    discounted_products = Product.objects.filter(discounted_price__isnull=False)

    return render(request, 'home.html', {
        'best_products': best_products,
        'discounted_products': discounted_products,
    })

def product_list(request):
    # Get all products by default
    products = Product.objects.all()

    # Get the selected category from query parameters
    category = request.GET.get('category')

    if category:
        # Filter products by category if a category is selected
        products = products.filter(category=category)

    # Get a list of unique categories for the dropdown
    categories = Product.objects.values_list('category', flat=True).distinct()

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
    })
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def contact_us(request):
    return render(request, 'contact_us.html')



def category_detail(request, category):
    # Fetch products belonging to the selected category
    products = Product.objects.filter(category=category)  # Ensure you're fetching products correctly
    return render(request, 'category_detail.html', {'category': category, 'products': products})

def category_context(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    return {'categories': categories}
    
@login_required(login_url='login')  # Redirect to the login page if not logged in
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user isn't logged in
    
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        cart_items = cart.cart_items.all()  # Use the correct related_name
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    context = {
        'username': request.user.username,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()

    # Calculate the total price for each cart item
    for item in cart_items:
        if item.product.discounted_price:
            item.total_price = item.product.discounted_price * item.quantity
        else:
            item.total_price = item.product.price * item.quantity
    
    # Calculate the total price for all items in the cart
    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'username': request.user.username,
    })

