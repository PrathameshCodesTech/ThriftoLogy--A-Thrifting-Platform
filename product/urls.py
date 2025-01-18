from django.urls import path
from product.views import Home,OuterWear,Top,Bottom,Kicks,ProductDetail,AddCart,ShowCart,update_cart_quantity,remove_from_cart,wishlist,add_to_wishlist,remove_from_wishlist


urlpatterns = [
    
    path('',Home , name='Home'),
    path('Outer-wear/',OuterWear,name="Outer-wear"),
    path('Top-wear/',Top,name="Top"),
    path('Bottom-wear/',Bottom,name="Bottom"),
    path('Kicks-wear/',Kicks,name="Kicks"),
   



    path('details/<int:pk>',ProductDetail.as_view(),name="Detail"),

    path('add-to-cart/',AddCart,name="Add_Cart"),
    path('cart/',ShowCart,name="Show_Cart"),

    path('update-cart/<int:cart_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:cart_id>/',remove_from_cart, name='remove_from_cart'),
   

    

    path('wishlist/',wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/',add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/',remove_from_wishlist, name='remove_from_wishlist'),


    
]