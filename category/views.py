from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm

# Create your views here.
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('category:list')
    else:
        form = CategoryForm()
        categories = Category.objects.all()  # Kategorileri al
        return render(request, 'category_create.html', {'form': form})

@login_required
def category_update(request, id):
    pass

@login_required
def category_delete(request, id):
    pass