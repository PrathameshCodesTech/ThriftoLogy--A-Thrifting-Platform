from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICE = (
    ('Gallery','Gallery'),
    ('Outerwear', 'Outerwear'),
    ('Top', 'Top'),
    ('Bottom', 'Bottom'),
    ('ChicKicks', 'ChicKicks'),
    ('Accessories', 'Accessories'),
)

class Product(models.Model):
    brand = models.CharField(max_length=55)
    name = models.CharField(max_length=255)
    description = models.TextField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=11)
    image = models.ImageField(upload_to='products/')
    video = models.FileField(upload_to='products/videos/', blank=True, null=True)
    material = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    era = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.brand})'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    

    # Below Property will be used by checkout.html page to show total cost in order summary
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    
#REVIEW - Extra

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} wishes for {self.product.name}'
    
    
