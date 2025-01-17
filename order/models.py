from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
from product.models import Product
from uuid import uuid4

STATUSCHOICE = [
    ('pending', 'Pending'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled')
]


class Order(models.Model):
    order_uuid = models.UUIDField(
        primary_key=True, max_length=128, auto_created=True, default=uuid4())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSCHOICE,
                              max_length=20, default='pending')
    order_on = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)


class OrderDetails(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)



# class OrderPlaced(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     ordered_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=50, choices=[
#         ('pending', 'Pending'),
#         ('shipped', 'Shipped'),
#         ('delivered', 'Delivered'),
#         ('cancelled', 'Cancelled')
#     ], default='pending')
