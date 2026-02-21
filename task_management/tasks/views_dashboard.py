from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def dashboard_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if user.groups.filter(name='Manager').exists():
        return redirect('manager_dashboard')
    elif user.groups.filter(name='Employee').exists():
        return redirect('employee_dashboard')
    else:
        return redirect('no_permission')
