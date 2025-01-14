# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from order.models import OrderPlaced, ShippingAddress
from customer.models import Customer
from product.models import Cart
from .forms import AddressSelectionForm, ShippingAddressForm
from product.models import Product
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings
from razorpay import Client
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
    customer = get_object_or_404(Customer,user = user)
    order_placed = OrderPlaced.objects.create(
          user = user,
          customer = customer,
          
    )
    client = Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    data ={"amount":total_amount,"currency":"INR","receipt":str()}
    client.order.create(data=data)
    return render(request, 'order/test.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items})


class ShippingAddressView(View):
     def get(self, request):
           form = ShippingAddressForm()
           return render(request, 'order/manualForm.html', {'form': form})

     def post(self, request):
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                user = request.user
                customer = form.cleaned_data['customer']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                zip_code = form.cleaned_data['zip_code']
                email = form.cleaned_data['email']
                ShippingAddress(user=user,customer=customer, phone=phone, address=address,
                                city=city, state=state, zip_code=zip_code, email=email).save()
                return render(request, 'order/test.html', {
                'customer':customer,
                'phone': phone,
                'address': address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'email': email
                })
            return render(request, 'order/manualForm.html', {'form': form})
    





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