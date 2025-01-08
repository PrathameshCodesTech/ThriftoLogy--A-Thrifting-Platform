from django.shortcuts import render,get_object_or_404,redirect
from product.models import Product,Cart
from django.views import View
from decimal import Decimal
from django.contrib import messages

def Home(request):
    products = Product.objects.filter(category="Gallery")
    brands = products.values_list('brand', flat=True).distinct()
    brand = request.GET.get('brand')
    if brand and brand != 'All':
        products = products.filter(brand=brand)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'low_to_high':
        products = products.order_by('selling_price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-selling_price')
    context = {
        'products': products,
        'brands': brands,
        'selected_brand': brand,
        'selected_sort': sort_by,
    }
    return render(request, 'product/clothesGallery.html', context)

def OuterWear(request):
    products = Product.objects.filter(category="Outerwear")
    brands = Product.objects.filter(category="Outerwear").values_list('brand', flat=True).distinct()
    
    # Handle brand filter
    brand = request.GET.get('brand')
    if brand and brand != 'All':
        products = products.filter(brand=brand)
    
    # Handle search query
    query = request.GET.get('query')
    if query and query!='None':
        products = products.filter(name__icontains=query)

    # Handle sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'low_to_high':
        products = products.order_by('selling_price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-selling_price')
    
    context = {
        'products': products,
        'brands': brands,
        'selected_brand': brand,  
        'selected_sort': sort_by,
        'query': query,
    }
    
    return render(request, "product/Outerwear.html", context)


class ProductDetail(View):
    def get(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        # Fetch similar products based on the same category
        similar_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
        context = {
            'product': product,
            'similar_products': similar_products,
        }
        return render (request,'product/detailPage.html',context)
    


def AddCart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
        
    # Check if the product is already in the cart
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        messages.info(request, 'Selected product is already in cart')
    else:
        Cart(user=user, product=product).save()
        
    return redirect('Show_Cart')


def ShowCart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = Decimal(0.0)  # Use Decimal for consistency
        shipping_amount = Decimal(70.0)  # Convert shipping amount to Decimal
        total_amount = Decimal(0.0)
        cart_product = Cart.objects.filter(user=user)  # Filter by user directly in the query
        
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)  # Assume discounted_price is Decimal
                amount += tempamount
            total_amount = amount + shipping_amount
        
        return render(request, 'cart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount})
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated
       