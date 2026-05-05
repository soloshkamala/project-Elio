from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm

def home(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    return render(request, 'accounts/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user, backend='accounts.backends.EmailOrUsernameModelBackend')
            messages.success(request, f"Вітаємо! Акаунт успішно створено.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)