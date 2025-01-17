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

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = Decimal('0.0')  # Initialize as Decimal
    shipping_amount = Decimal('70.0')  # Convert shipping amount to Decimal
    total_amount = Decimal('0.0')  # Initialize as Decimal
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            # Ensure discounted_price is Decimal
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        total_amount = amount + shipping_amount




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

    return render(request, 'order/test.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items})



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
      

# from uuid import uuid4
# from decimal import Decimal
# from django.shortcuts import redirect
# import razorpay
# from django.conf import settings

# @login_required
# def checkout(request):
#     user = request.user
#     add = Customer.objects.filter(user=user)
#     cart_items = Cart.objects.filter(user=user)

#     # Calculate total amount
#     amount = Decimal('0.0')
#     shipping_amount = Decimal('70.0')
#     total_amount = Decimal('0.0')

#     if cart_items:
#         for item in cart_items:
#             amount += item.quantity * item.product.discounted_price
#         total_amount = amount + shipping_amount

#     # Create Order
#     order = Order.objects.create(
#         user=user,
#         total=total_amount,
#     )

#     # Create OrderDetails for each cart item
#     for item in cart_items:
#         OrderDetails.objects.create(
#             order_id=order,
#             product=item.product,
#             quantity=item.quantity,
#             price=item.product.discounted_price,
#         )

#     # Create Razorpay order
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#     razorpay_order = client.order.create({
#         'amount': int(total_amount * 100),  # Amount in paisa
#         'currency': 'INR',
#         'payment_capture': '1'
#     })

#     # Save Razorpay order ID to the Order for verification
#     order.razorpay_order_id = razorpay_order['id']
#     order.save()

#     # Pass details to template
#     return render(request, 'order/test.html', {
#         'add': add,
#         'cart_items': cart_items,
#         'total_amount': total_amount,
#         'razorpay_order_id': razorpay_order['id'],
#         'razorpay_key_id': settings.RAZORPAY_KEY_ID,
#     })


# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseBadRequest

# @csrf_exempt
# def payment_done(request):
#     if request.method == "POST":
#         try:
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')

#             # Verify Razorpay signature
#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#             client.utility.verify_payment_signature({
#                 'razorpay_order_id': order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             })

#             # Update the Order status
#             order = Order.objects.get(razorpay_order_id=order_id)
#             order.status = 'paid'
#             order.save()

#             # Clear the cart
#             Cart.objects.filter(user=order.user).delete()

#             return render(request, 'order/success.html', {'order': order})
#         except razorpay.errors.SignatureVerificationError:
#             return HttpResponseBadRequest("Invalid Payment Signature")
#         except Order.DoesNotExist:
#             return HttpResponseBadRequest("Order not found")
#     return HttpResponseBadRequest("Invalid Request")
