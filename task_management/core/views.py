from django.shortcuts import render

# Create your views here.
def home(request):
    # Clear any cached user state and render the home page
    context = {
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'home.html', context)

def no_permission(request):
    if not request.user.is_authenticated:
        from django.urls import reverse
        login_url = reverse('sign_in')
        next_url = request.get_full_path()
        return redirect(f'{login_url}?next={next_url}')
    return render(request, 'no_permission.html')