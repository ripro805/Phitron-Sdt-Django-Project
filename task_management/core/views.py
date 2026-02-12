from django.shortcuts import render

# Create your views here.
def home(request):
    # Clear any cached user state and render the home page
    context = {
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'home.html', context)

def no_permission(request):
    return render(request, 'no_permission.html')