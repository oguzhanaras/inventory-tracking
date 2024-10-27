from django import template

register = template.Library()

@register.filter
def unit_price(sale_price, quantity):
    if quantity > 0:
        return sale_price / quantity
    return 0
