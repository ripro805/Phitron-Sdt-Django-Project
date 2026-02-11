from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import TaskForm, TaskModelForm,TaskDetailModelForm
from tasks.models import Employee, Task,TaskDetail, Project
from datetime import date
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required

# Create your views here.

def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()


@user_passes_test(is_manager, login_url='no_permission')     
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

@user_passes_test(is_employee, login_url='no_permission')
def employee_dashboard(request):
    return render(request,'dashboard/employee_dashboard.html')

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
@login_required
@permission_required('tasks.add_task', raise_exception=True)
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

@login_required
@permission_required('tasks.change_task', raise_exception=True)
def update_task(request,id):
   # employees=Employee.objects.all()
    task=Task.objects.get(id=id)
    task_form=TaskModelForm(instance=task) #get request
    task_detail_form=None
    if task.detail:
      task_detail_form=TaskDetailModelForm(instance=task.detail)
    if request.method=='POST':
        task_form=TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST, instance=task.detail)
        if task_form.is_valid() and task_detail_form.is_valid():
            # Process the form data
            #For Model Form
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, 'Task updated successfully!')
            return redirect('manager-dashboard')  # Redirect after successful submission  
    return render(request,'task_form.html',{'task_form':task_form,'task_detail_form':task_detail_form})
@login_required
@permission_required('tasks.view_task', raise_exception=True)
def view_tasks(request):
   #task_count=Task.objects.aggregate(total=Count('id'))['total']
   projects=Project.objects.annotate(num_task=Count('task')).order_by('num_task')
   return render(request,'show_tasks.html',{"projects":projects})

@login_required
@permission_required('tasks.delete_task', raise_exception=True)
def delete_task(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('manager-dashboard')
    return render(request, 'confirm_delete.html', {'task': task})