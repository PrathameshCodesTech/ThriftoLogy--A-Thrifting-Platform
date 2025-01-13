from django import template
register = template.Library()

@register.filter
def grandTotal(value):
    result = 0
    for i in value:
        result += (i.cart_product.product_price * i.quantity)
    return result