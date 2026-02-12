from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm, CustomizeRegisterForm,LoginForm, AssignRoleForm,CreateGroupForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login , logout
from django.shortcuts import redirect
from django.contrib import messages
from users.forms import StyledAuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch


# Create your views here.

#test for user
def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser

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
           

@login_required           
def sign_out(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


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


@user_passes_test(is_admin,login_url='no_permission')    
def admin_dashboard(request):
    users = User.objects.only('id', 'first_name', 'last_name', 'email').prefetch_related(
        Prefetch('groups', queryset=Group.objects.only('id', 'name'))
    ).order_by('-date_joined')
    
    # Use prefetched data - no additional queries
    for user in users:
        groups = list(user.groups.all())  # Uses prefetched cache
        user.group_name = groups[0].name if groups else "No Group Assigned"
    return render(request, 'admin/admin_dashboard.html', {'users': users})    
@user_passes_test(is_admin,login_url='no_permission')    
def assign_role(request, user_id):
    user = User.objects.prefetch_related('groups').get(id=user_id)
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
@user_passes_test(is_admin,login_url='no_permission')    
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group= form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('create_group')
    return render(request, 'admin/create_group.html', {'form': form})
@user_passes_test(is_admin,login_url='no_permission')    
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})