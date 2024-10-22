from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib import messages

# Kayıt olma fonksiyonu
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kayıt başarılı! Giriş yapabilirsiniz.")
            return redirect('users:login')
        else:
            messages.error(request, "Kayıt sırasında hata oluştu. Lütfen tekrar deneyin.")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Giriş yapma fonksiyonu
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product:index')
            else:
                messages.error(request, "Kullanıcı adı veya şifre hatalı.")
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
