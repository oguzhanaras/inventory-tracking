from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from sale.models import Sale, SaleItem
from django.db.models import Sum, F


# Ana sayfa
def index(request):
    # 1. Toplam Satış Sayısı ve Toplam Gelir
    total_sales_count = Sale.objects.filter(user=request.user).count()
    total_revenue = Sale.objects.filter(user=request.user).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # 2. Toplam Kâr
    # Satılan ürünlerin maliyeti hesaplanır
    total_cost = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .annotate(total_cost=F('product__cost_price') * F('quantity'))
        .aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0
    )
    total_profit = total_revenue - total_cost

    # 3. En Çok Satılan Ürün
    top_selling_product = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')
        .first()
    )
    top_product_name = top_selling_product['product__name'] if top_selling_product else "Yok"

    # 4. Aylık Gelir Verisi (Grafik için)
    monthly_revenue = []
    for month in range(1, 13):
        monthly_sales = Sale.objects.filter(user=request.user, sale_date__month=month)
        monthly_revenue.append(monthly_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0)

    # Context verilerini tanımla
    context = {
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'top_product_name': top_product_name,
        'monthly_revenue': monthly_revenue,
    }

    return render(request, 'index.html', context)

@login_required
def product(request):
    user_products = Product.objects.filter(owner=request.user)
    return render(request, 'product.html', {'products': user_products})

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('inventory:product')
    else:
        form = ProductForm()

    categories = Category.objects.all()  # Kategorileri al
    return render(request, 'create_product.html', {'form': form, 'categories': categories})

@login_required
def view_product(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'view_product.html', {'product': product})

@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()  # Tüm kategorileri alıyoruz

    if request.method == "POST":
        # Form verilerini güncelle
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.cost_price = request.POST['cost_price']
        product.sale_price = request.POST['sale_price']
        product.quantity = request.POST['quantity']
        product.category_id = request.POST['category']
        
        product.save()

        return redirect('inventory:view_product', id=product.id)
    
    return render(request, 'edit_product.html', {'product': product, 'categories': categories})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()

    return redirect('inventory:product')