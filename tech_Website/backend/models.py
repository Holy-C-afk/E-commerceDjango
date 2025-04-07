from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('home_appliances', 'Home Appliances'),
        ('books', 'Books'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    stock_quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

    def is_on_discount(self):
        """Returns True if product has a discounted price."""
        return self.discounted_price is not None
    
    
    def get_discounted_price(self):
        """Returns discounted price if exists."""
        if self.is_on_discount():
            return self.discounted_price
        return self.price
    
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem", related_name="carts")  # Add related_name

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')  # Use related_name here
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.name
