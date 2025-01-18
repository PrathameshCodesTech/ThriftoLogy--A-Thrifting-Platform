# urls.py
from django.urls import path
from order.views import checkout,payment_handler
#payment_done

urlpatterns = [

    path('check-out/',checkout,name="Check_out"),


    path('payment-handler/', payment_handler, name="payment_handler"),

    
    # path('proceed-to-pay/<str:cart_items>/<int:total>/<str:address>',proceed_to_pay,name="ProceedToPay")

    # path('paymentdone/',payment_done, name='payment_done'),
]