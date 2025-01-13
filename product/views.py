from django.shortcuts import render,get_object_or_404,redirect
from product.models import Product,Cart,Wishlist
from django.views import View
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


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
        products = products.filter(brand__icontains=query) or products.filter(name__icontains=query)

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
        print(product)
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
    try:
        product = Product.objects.get(id=product_id)
        
        # Check if the product is already in the cart
        cart_item = Cart.objects.filter(user=user, product=product).first()
        if cart_item:
            messages.info(request, 'Selected product is already in cart')
        else:
            Cart(user=user, product=product).save()
            messages.success(request, 'Product added to cart successfully!')
    except Product.DoesNotExist:
        pass

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
        
        return render(request, 'product/cart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount})


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
        
        return render(request, 'product/cart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount})
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated
       

    
def update_cart_quantity(request, cart_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    action = request.POST.get('action')
    
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                messages.warning(request, 'Quantity cannot be less than 1')
                
        cart_item.save()
        messages.success(request, 'Cart updated successfully!')
        
    except Cart.DoesNotExist:
        messages.error(request, 'Cart item not found')
    
    return redirect('Show_Cart')

def remove_from_cart(request, cart_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        cart_item.delete()
        messages.success(request, 'Product removed from cart successfully!')
        
    except Cart.DoesNotExist:
        messages.error(request, 'Cart item not found')
    
    return redirect('Show_Cart')

def calculate_cart_totals(user):
    cart_items = Cart.objects.filter(user=user)
    amount = Decimal('0.0')
    shipping_amount = Decimal('70.0')
    
    for item in cart_items:
        amount += item.quantity * item.product.discounted_price
    
    total_amount = amount + shipping_amount
    return amount, total_amount




@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'product/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, 'Product added to wishlist successfully!')
    except:
        messages.info(request, 'Product is already in your wishlist!')
    
    # Return to previous page
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, 'Product removed from wishlist!')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))