from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
    list_filter = ['state', 'city']
    search_fields = ['user__username', 'name', 'city', 'state', 'zipcode']

