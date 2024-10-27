# sales/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Sale, SaleItem
from inventory.models import Product
from django.contrib.auth.decorators import login_required
from django.db import transaction


@login_required
def sale_list(request):
    sales = Sale.objects.filter(user=request.user)
    return render(request,'sale_list.html', {'sales': sales})

@login_required
@transaction.atomic
def create_sale(request):
    products = Product.objects.filter(owner=request.user)  # Kullanıcının ürünlerini çek

    if request.method == "POST":
        user = request.user
        quantities = request.POST.getlist('quantities')  # Miktarlar aynı sırada alınacak

        sale = Sale.objects.create(user=user, total_price=0.00)
        total_price = 0
        
        for product_id, quantity in zip(products.values_list('id', flat=True), quantities):
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)

            if quantity > 0:  # Sadece pozitif miktarları dikkate al
                sale_price = product.sale_price * quantity
                SaleItem.objects.create(sale=sale, product=product, quantity=quantity, sale_price=sale_price)
                total_price += sale_price

        sale.total_price = total_price
        sale.save()

        return redirect('sales:sale_list')

    return render(request, 'create_sale.html', {'products': products})
