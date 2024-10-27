from django.db import models, transaction
from django.contrib.auth import get_user_model
from inventory.models import Product
from django.core.exceptions import ValidationError

User = get_user_model()


class Sale(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        help_text="User who made the sale."
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        help_text="Total price of the sale."
    )
    sale_date = models.DateTimeField(
        auto_now_add=True, 
        help_text="Date when the sale was made."
    )

    def __str__(self):
        return f'Sale by {self.user} on {self.sale_date}'


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale, 
        on_delete=models.CASCADE, 
        related_name="items", 
        help_text="Sale to which this item belongs."
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        help_text="Product sold."
    )
    quantity = models.PositiveIntegerField(
        help_text="Quantity of the product sold."
    )
    sale_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Sale price of the product."
    )

    def save(self, *args, **kwargs):
        if self.quantity > self.product.quantity:
            raise ValidationError("Sale quantity cannot exceed available stock.")

        # Güncelleme işlemini atomic bir işlem olarak yaparak veri tutarlılığı sağlıyoruz
        with transaction.atomic():
            # Ürün stok miktarını güncelle
            self.product.quantity -= self.quantity
            self.product.save()
            
            # SaleItem kaydını kaydet
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} (Sale: {self.sale.id})'
