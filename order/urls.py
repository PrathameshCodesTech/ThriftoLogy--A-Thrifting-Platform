from django.urls import path
from order.views import index

urlpatterns = [
    path('',index, name='index'),  
]