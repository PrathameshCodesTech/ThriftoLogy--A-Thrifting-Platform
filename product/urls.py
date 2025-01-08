from django.urls import path
from product.views import Home,OuterWear,ProductDetail,AddCart,ShowCart

urlpatterns = [
    path('',Home , name='Home'),
    path('Outer-wear/',OuterWear,name="Outer-wear"),
    path('details/<int:pk>',ProductDetail.as_view(),name="Detail"),

    path('add-to-cart/',AddCart,name="Add_Cart"),
    path('cart/',ShowCart,name="Show_Cart"),
   
]