from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import TaskForm, TaskModelForm,TaskDetailModelForm
from tasks.models import Employee, Task,TaskDetail, Project
from datetime import date
from django.db.models import Q, Count
from django.contrib import messages

# Create your views here.
def manager_dashboard(request):
    type=request.GET.get('type', 'all')    
    # print("Type is:",type)
   
 
    counts=Task.objects.aggregate(total=Count('id'),
                                 pending=Count('id', filter=Q(status='PENDING')),
                                 completed=Count('id', filter=Q(status='COMPLETED')),
                                 inprogress=Count('id', filter=Q(status='IN_PROGRESS'))
                                 
    )
    #Retriving task data based on type
    base_Query=Task.objects.select_related('detail').prefetch_related('assigned_to')
    if type=='pending':
        tasks=base_Query.filter(status='PENDING')
    elif type=='completed':
        tasks=base_Query.filter(status='COMPLETED')
    elif type=='inprogress':
        tasks=base_Query.filter(status='IN_PROGRESS')
    elif type=='all':
        tasks=base_Query.all()
    context={
        'tasks':tasks,  # Added tasks to context
        'counts':counts,
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
    task_form=TaskModelForm() #get request
    task_detail_form=TaskDetailModelForm()
    if request.method=='POST':
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            # Process the form data
            #For Model Form
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, 'Task created successfully!')
            return redirect('create-task')  # Redirect after successful submission  
    return render(request,'task_form.html',{'task_form':task_form,'task_detail_form':task_detail_form})

def view_tasks(request):
   #task_count=Task.objects.aggregate(total=Count('id'))['total']
   projects=Project.objects.annotate(num_task=Count('task')).order_by('num_task')
   return render(request,'show_tasks.html',{"projects":projects})