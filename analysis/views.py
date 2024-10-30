from django.shortcuts import render
from sale.models import Sale, SaleItem
from inventory.models import Product
from django.db.models import Sum, F
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

@login_required
def user_analysis(request):
    # Kullanıcının satış ve envanter bilgilerini al
    user_sales = Sale.objects.filter(user=request.user)
    user_inventory = Product.objects.filter(owner=request.user)

    # 1. Toplam Satış Sayısı ve Gelir Analizi
    total_sales_count = user_sales.count()
    total_revenue = user_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # 2. Müşteri Başına Ortalama Sipariş Değeri
    average_order_value = total_revenue / total_sales_count if total_sales_count else 0

    # 3. En Çok Satılan Ürün Analizi
    top_selling_products = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    # 4. En Yüksek Gelir Getiren Ürünler
    top_revenue_products = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .values('product__name')
        .annotate(total_revenue=Sum(F('sale_price') * F('quantity')))
        .order_by('-total_revenue')[:5]
    )

    # 5. Stok Tükenme Analizi
    low_stock_products = user_inventory.filter(quantity__lt=10).values('name', 'quantity')

    # 6. Kar-Zarar Analizi
    # Sadece satılan ürünlerin maliyetini hesapla
    sold_items_cost = (
    SaleItem.objects
    .filter(sale__user=request.user)
    .aggregate(total_cost=Sum(F('product__cost_price') * F('quantity')))['total_cost'] or 0
    )

    # Sadece satılan ürünlerin maliyeti üzerinden kar oranını hesapla
    profit_margin = round(((total_revenue - sold_items_cost) / total_revenue) * 100, 2) if total_revenue else 0


    # 7. Satışların Kategori Bazında Yüzdesel Dağılımı
    category_distribution = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .values('product__category__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')
    )
    total_sold_items = sum(item['total_sold'] for item in category_distribution) or 1
    category_distribution = [
        {
            'category': item['product__category__name'],
            'percentage': (item['total_sold'] / total_sold_items) * 100
        }
        for item in category_distribution
    ]

    # 8. Aylık Kar Verileri
    monthly_profit_data = []
    for month in range(1, 13):
        month_sales = user_sales.filter(sale_date__month=month)
        monthly_revenue = month_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
        monthly_cost = (
            SaleItem.objects
            .filter(sale__user=request.user, sale__sale_date__month=month)
            .aggregate(monthly_cost=Sum(F('product__cost_price') * F('quantity')))['monthly_cost'] or 0
        )
        profit = monthly_revenue - monthly_cost
        monthly_profit_data.append({
            'month': datetime(2000, month, 1).strftime('%B'),
            'profit': profit
        })

    # 9. Günlük Kar Verileri (Son 7 Gün)
    daily_profit_data = []
    today = datetime.today()
    for day in range(7):  # Son 7 gün için
        day_date = today - timedelta(days=day)
        day_sales = user_sales.filter(sale_date__date=day_date.date())
        daily_revenue = day_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
        daily_cost = (
            SaleItem.objects
            .filter(sale__user=request.user, sale__sale_date__date=day_date.date())
            .aggregate(daily_cost=Sum(F('product__cost_price') * F('quantity')))['daily_cost'] or 0
        )
        daily_profit = daily_revenue - daily_cost
        daily_profit_data.append({
            'day': day_date.strftime('%d %B'),
            'profit': daily_profit
        })

    # 10. Aylık Büyüme Oranı
    previous_month_sales = user_sales.filter(sale_date__month=(datetime.now().month - 1)).aggregate(Sum('total_price'))['total_price__sum'] or 0
    growth_rate = ((total_revenue - previous_month_sales) / previous_month_sales * 100) if previous_month_sales else 0

    # 11. Stok Dönüşüm Hızı
    turnover_rate = total_sales_count / user_inventory.count() if user_inventory.count() else 0

    # 12. En Az Satılan Ürünler
    low_selling_products = (
        SaleItem.objects
        .filter(sale__user=request.user)
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('total_sold')[:5]
    )

    context = {
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'total_cost': sold_items_cost,
        'profit_margin': profit_margin,
        'average_order_value': average_order_value,
        'growth_rate': growth_rate,
        'turnover_rate': turnover_rate,
        'top_selling_products': top_selling_products,
        'top_revenue_products': top_revenue_products,
        'low_stock_products': low_stock_products,
        'category_distribution': category_distribution,
        'profit_data': monthly_profit_data,
        'daily_profit_data': daily_profit_data[::-1],
        'low_selling_products': low_selling_products,
    }

    return render(request, 'user_analysis.html', context)
