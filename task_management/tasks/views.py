from django.shortcuts import render
from django.http import HttpResponse
from .forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

# Create your views here.
def manager_dashboard(request):
    return render(request,'dashboard/manager_dashboard.html')
def user_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

def test(request):
    names = ["Mahmud", "Ahamed", "John", "Mr. X"]
    count = 0
    for name in names:
        count += 1
    context = {
        "names": names,
        "age": 23,
        "count": count
    }
    return render(request, 'test.html', context)

def create_task(request):
   # employees=Employee.objects.all()
    form=TaskModelForm() #get request
    if request.method=='POST':
        form=TaskModelForm(request.POST)
        if form.is_valid():
            # Process the form data
            #For Model Form
            form.save()
            return render(request, "task_form.html", {"form": form, "message": "Task Created Successfully"})
       
        return HttpResponse("Task Created Successfully")   
    context={'form':form}
    return render(request, 'task_form.html', context)

def view_tasks(request):
    #retrive all tasks
    tasks=Task.objects.all()
    #retrive a specific tasks 
    task_3=Task.objects.get(pk=3)
    #Fetch first task
    first_task=Task.objects.first()

    return render(request,'show_tasks.html',{"tasks":tasks,"task_3":task_3,"first_task":first_task})