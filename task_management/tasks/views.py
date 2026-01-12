from django.shortcuts import render
from django.http import HttpResponse
from .forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task,TaskDetail, Project
from datetime import date
from django.db.models import Q, Count

# Create your views here.
def manager_dashboard(request):
    tasks=Task.objects.all()
    #getting task count
    total_task=tasks.count()
    pending_task=tasks.filter(status='Pending').count()
    completed_task=tasks.filter(status='Completed').count()
    inprogress_task=tasks.filter(status='In Progress').count()
    context={
        'tasks':tasks,  # Added tasks to context
        'total_task':total_task,
        'pending_task':pending_task,
        'completed_task':completed_task,
        'inprogress_task':inprogress_task
    }
    return render(request,'dashboard/manager_dashboard.html', context)


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
   #task_count=Task.objects.aggregate(total=Count('id'))['total']
   projects=Project.objects.annotate(num_task=Count('task')).order_by('num_task')
   return render(request,'show_tasks.html',{"projects":projects})