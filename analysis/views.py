from django.shortcuts import render
from sale.models import Sale, SaleItem
from inventory.models import Product
from django.db.models import Sum, F
from datetime import datetime

def user_analysis(request):
    # Kullanıcının satış ve envanter bilgilerini al
    user_sales = Sale.objects.filter(user=request.user)
    user_inventory = Product.objects.filter(owner=request.user)

    # 1. Toplam Satış Sayısı ve Gelir Analizi
    total_sales_count = user_sales.count()
    total_revenue = user_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # 2. En Çok Satılan Ürün Analizi
    top_selling_products = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]  # İlk 5 ürünü listele
    )

    # 3. Stok Tükenme Analizi (Stok Miktarı 10'un altında olan ürünler)
    low_stock_products = user_inventory.filter(quantity__lt=10).values('name', 'quantity')

    # 4. Kar-Zarar Analizi: Satılan ürünlerin maliyetini hesapla
    sold_items_cost = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .aggregate(total_cost=Sum(F('product__cost_price') * F('quantity')))['total_cost'] or 0
    )

    # Sadece satılan ürünlerin maliyetine göre kar oranı
    profit_margin = round(((total_revenue - sold_items_cost) / total_revenue) * 100, 2) if total_revenue else 0

    # 5. Satışların Kategori Bazında Yüzdesel Dağılımı
    category_distribution = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .values('product__category__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')
    )
    
    # Toplam satılan ürün sayısını hesapla
    total_sold_items = sum(item['total_sold'] for item in category_distribution) or 1
    
    # Yüzdesel dağılımı hesapla
    category_distribution = [
        {
            'category': item['product__category__name'],
            'percentage': (item['total_sold'] / total_sold_items) * 100
        }
        for item in category_distribution
    ]

    # 6. Kar Verileri Analizi (Aylık)
    monthly_profit_data = []
    for month in range(1, 13):
        month_sales = user_sales.filter(sale_date__month=month)
        monthly_revenue = month_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Satılan ürünlerin aylık maliyetini hesapla
        monthly_cost = (
            SaleItem.objects
            .filter(sale__user=request.user, sale__sale_date__month=month)
            .aggregate(monthly_cost=Sum(F('product__cost_price') * F('quantity')))['monthly_cost'] or 0
        )
        
        profit = monthly_revenue - monthly_cost
        monthly_profit_data.append({
            'month': datetime(2000, month, 1).strftime('%B'),  # Ay adı
            'profit': profit
        })
    
    # Analiz sonuçlarını context'e ekle
    context = {
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'total_cost': sold_items_cost,  # Sadece satılan ürünlerin maliyeti
        'profit_margin': profit_margin,  # Yuvarlanmış kar oranı
        'top_selling_products': top_selling_products,
        'low_stock_products': low_stock_products,
        'category_distribution': category_distribution,
        'profit_data': monthly_profit_data,  # Kar verilerini ekle
    }

    return render(request, 'user_analysis.html', context)
