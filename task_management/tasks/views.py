from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to Task Management System")
def contact(request):
    return HttpResponse("<h1 style ='color:aqua'>This is  Contact Page </h1>")
    
def  show_tasks(request):
    return HttpResponse("This is Our page")