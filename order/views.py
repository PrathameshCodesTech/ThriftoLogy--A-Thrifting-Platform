# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from order.models import OrderDetails,Order
from customer.models import Customer
from product.models import Cart
from product.models import Product
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings
from razorpay import Client
import pkg_resources

# @login_required
# def checkout(request):
#     user = request.user
#     add = Customer.objects.filter(user=user)
#     cart_items = Cart.objects.filter(user=user)
#     amount = Decimal('0.0')  # Initialize as Decimal
#     shipping_amount = Decimal('70.0')  # Convert shipping amount to Decimal
#     total_amount = Decimal('0.0')  # Initialize as Decimal
#     cart_product = [p for p in Cart.objects.all() if p.user == user]
#     if cart_product:
#         for p in cart_product:
#             # Ensure discounted_price is Decimal
#             tempamount = p.quantity * p.product.discounted_price
#             amount += tempamount
#         total_amount = amount + shipping_amount




    #hitesh here
    # customer = get_object_or_404(Customer,user = user)
    # order_placed = OrderPlaced.objects.create(
    #       user = user,
    #       customer = customer,
          
    # )
    # client = Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    # data ={"amount":total_amount,"currency":"INR","receipt":str()}
    # client.order.create(data=data)

    # hitesh END here!

    # return render(request, 'order/test.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items})



# Vassi here!

# def proceed_to_pay(request,cart_items,total,add):
#     user = request.user
#     total = total
#     ship=add
#     fo=Order.create(user=user,total=total,shipping_address=ship)
#     fo.save()
#     idd=fo.id

#     for i in cart_items:
#          pro=Product.objects.filter(id=i.id)
#          OrderDetails(order_id=idd,product=pro,quantity=i.quantity,price=total).save
#     return redirect('Home')
      


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    
    amount = Decimal('0.0')
    shipping_amount = Decimal('70.0')
    total_amount = Decimal('0.0')
    
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        total_amount = amount + shipping_amount

    # Convert to paise for Razorpay (1 INR = 100 paise)
    razorpay_amount = int(total_amount * 100)

    # Razorpay Client Setup
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create Razorpay Order
    razorpay_order = client.order.create({
        "amount": razorpay_amount,  # Razorpay accepts amount in paise
        "currency": "INR",
        "payment_capture": "1"  # Automatic capture
    })
    
    # Pass the Razorpay order details to template
    context = {
        'add': add,
        'total_amount': total_amount,
        'razorpay_amount': razorpay_amount,
        'cart_items': cart_items,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'currency': "INR",
        'callback_url': '/payment-handler/'
    }
    
    return render(request, 'order/test.html', context)


@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        try:
            # Verify Razorpay payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': request.POST.get('razorpay_order_id'),
                'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                'razorpay_signature': request.POST.get('razorpay_signature')
            }
            client.utility.verify_payment_signature(params_dict)
            
            # Payment successful, update order status
            return JsonResponse({'status': 'Payment successful!'})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'Payment verification failed.'})
    return JsonResponse({'status': 'Invalid request.'})
