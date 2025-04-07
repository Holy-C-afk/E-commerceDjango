from .models import Product

def categories_processor(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    return {'categories': categories}
