from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from users.forms import RegisterForm, CustomizeRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout
from django.shortcuts import redirect
from django.contrib import messages
from users.forms import StyledAuthenticationForm
from users. forms import LoginForm



# Create your views here.
def sign_up(request):
    if request.method == 'GET':
        form = CustomizeRegisterForm()
    elif request.method == 'POST':
        form = CustomizeRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active=False
            user.save()
            messages.success(request, " confirmation email has been sent to your email address. Please activate your account.")
            return redirect('sign_in')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    return render(request, 'registration/register.html',{'form': form})


def sign_in(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request=request,data=request.POST)
        if form.is_valid():
           user=form.get_user()
           auth_login(request, user)
           return redirect('home')
    return render(request, 'registration/login.html', {'form': form})
           

           
def sign_out(request):
    form = StyledAuthenticationForm()
    if request.method == 'POST':
        form = StyledAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})


