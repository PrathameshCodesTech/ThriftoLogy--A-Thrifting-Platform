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
# from django.conf import settings
# from razorpay import Client
# import pkg_resources

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
    return render(request, 'order/test.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items})


def proceed_to_pay(request,cart_items,total,add):
    user = request.user
    total = total
    ship=add
    fo=Order.create(user=user,total=total,shipping_address=ship)
    fo.save()
    idd=fo.id

    for i in cart_items:
         pro=Product.objects.filter(id=i.id)
         OrderDetails(order_id=idd,product=pro,quantity=i.quantity,price=total).save
    return redirect('Home')
      

@login_required
def payment_done(request):
	custid = request.GET.get('custid')
	print("Customer ID", custid)
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	for cid in cartid:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
	return redirect("orders")