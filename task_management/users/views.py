from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from users.forms import RegisterForm, CustomizeRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout
from django.shortcuts import redirect
from django.contrib import messages
from users.forms import StyledAuthenticationForm
from users. forms import LoginForm
from django.contrib.auth.tokens import default_token_generator


# Create your views here.
def sign_up(request):
    if request.method == 'GET':
        form = CustomizeRegisterForm()
    elif request.method == 'POST':
        form = CustomizeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, "A confirmation email has been sent to your email address. Please activate your account.")
            return redirect('sign_in')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    return render(request, 'registration/register.html', {'form': form})


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


def activate_account(request, uid, token):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        messages.error(request, "Invalid activation link.")
        return redirect('sign_in')

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully. You can now log in.")
        return redirect('sign_in')
    else:
        messages.error(request, "Invalid or expired activation link.")
        return redirect('sign_in')
    
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')    