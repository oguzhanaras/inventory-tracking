from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from sale.models import Sale, SaleItem
from django.db.models import Sum, F


# Ana sayfa
def index(request):
    return render(request, 'index.html')

@login_required
def product(request):
    user_products = Product.objects.filter(owner=request.user, is_active=True)
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
    product.is_active = False  # Ürünü inaktif yap
    product.save()

    return redirect('inventory:product')
