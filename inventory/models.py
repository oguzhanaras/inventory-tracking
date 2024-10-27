from django.db import models
from django.contrib.auth.models import User
from category.models import Category


class Product(models.Model):
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        help_text="Product owner."
    )
    name = models.CharField(
        max_length=100, 
        help_text="Product name."
    )
    description = models.TextField(
        help_text="Detailed product description."
    )
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Product cost price."
    )
    sale_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Product sale price."
    )
    quantity = models.PositiveIntegerField(
        default=0, 
        help_text="Quantity available in stock."
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        help_text="Product category."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="Creation timestamp."
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        help_text="Last update timestamp."
    )
    deleted_at = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="Timestamp when the product was deleted, if applicable."
    )

    def __str__(self):
        return f'{self.name} ({self.category})'
