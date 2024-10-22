from django.db import models
from django.contrib.auth.models import User
from category.models import Category


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user who owns the product.")
    name = models.CharField(max_length=100, help_text="Name of the product.")
    description = models.TextField(help_text="Description of the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product.")
    quantity = models.PositiveIntegerField(default=0, help_text="Available quantity of the product.")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Category of the product.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the product was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the product was last updated.")
    deleted_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the product was deleted.")

    def __str__(self):
        return self.name
