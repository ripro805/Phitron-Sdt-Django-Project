from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm, CustomizeRegisterForm,LoginForm, AssignRoleForm,CreateGroupForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout
from django.shortcuts import redirect
from django.contrib import messages
from users.forms import StyledAuthenticationForm
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
    users = User.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'users': users})    

def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()  # Clear existing roles
            user.groups.add(role)  # Assign new role
            user.save()
            messages.success(request, f"Role '{role.name}' has been assigned to {user.username}.")
            return redirect('admin_dashboard')
    
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})

def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group= form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {'form': form})