from django.contrib import admin
from .models import OrderPlaced, ShippingAddress

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']
    list_filter = ['status', 'ordered_date']
    search_fields = ['user__username', 'customer__name', 'product__name']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'order', 'address', 'city', 'state', 'zip_code', 'phone', 'email']
    list_filter = ['state', 'city']
    search_fields = ['user__username', 'customer__name', 'address', 'city', 'state', 'zip_code']