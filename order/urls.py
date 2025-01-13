# urls.py
from django.urls import path
from order.views import checkout,OrderPlaced,ShippingAddressView

urlpatterns = [
    path('check-out/',checkout,name="Check_out"),
    path('order-out/',OrderPlaced,name="OrderPlaced"),
    path('address-out/',ShippingAddressView.as_view(),name="ShippingAddressView"), 
]