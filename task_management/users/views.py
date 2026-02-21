from django.views.generic import TemplateView
# Base profile view using TemplateView

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm, CustomizeRegisterForm,LoginForm, AssignRoleForm,CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login , logout
from django.shortcuts import redirect
from django.contrib import messages
from users.forms import StyledAuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

# Class-based logout view
  # Optional: customize logout page

#test for user
def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser

def send_activation_email(user, activation_link):
    subject = 'Activate Your TaskPro Account'
    html_content = render_to_string('accounts/activation_email.html', {
        'activation_link': activation_link,
        'year': 2026,
    })
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        'noreply@taskpro.com',
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def sign_up(request):
    if request.method == 'GET':
        form = CustomizeRegisterForm()
    elif request.method == 'POST':
        form = CustomizeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Generate activation link
            from django.contrib.sites.shortcuts import get_current_site
            from django.urls import reverse
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"http://{current_site.domain}{reverse('activate_account', args=[uid, token])}"
            send_activation_email(user, activation_link)
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
           
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    def get_success_url(self):
        next_url=self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
class CustomLogoutView(LogoutView):
    next_page = "home"  # Redirect to home after logout

# Password change views
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = '/users/password_change/done/'

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

# Password change views
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    form_class = CustomPasswordChangeForm
    success_url = '/users/password_change/done/'

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

# Password reset views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/password_reset_email.html'
    html_email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/users/password_reset/done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = '/users/password_reset/complete/'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
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


@user_passes_test(is_admin,login_url='sign_in')    
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

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = getattr(user, 'profile', None)
        context['user'] = user
        context['profile'] = profile
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        # Add user roles (group names)
        context['roles'] = list(user.groups.values_list('name', flat=True))
        return context
        return context