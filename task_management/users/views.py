from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from users.forms import RegisterForm, CustomizeRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect


# Create your views here.
def sign_up(request):
    from django.contrib import messages
    if request.method == 'GET':
        form = CustomizeRegisterForm()
    elif request.method == 'POST':
        form = CustomizeRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    return render(request, 'registration/register.html',{'form': form})


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')


