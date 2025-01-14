# urls.py
from django.urls import path
from order.views import checkout,proceed_to_pay

urlpatterns = [
    path('check-out/',checkout,name="Check_out"),

    # path('address-out/',ShippingAddressView.as_view(),name="ShippingAddressView"),
    path('proceed-to-pay/<str:cart_items>/<int:total>/<str:address>',proceed_to_pay,name="ProceedToPay")
]