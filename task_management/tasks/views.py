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
    # Get tasks assigned to the current employee
    try:
        employee = Employee.objects.get(email=request.user.email)
        my_tasks = Task.objects.filter(assigned_to=employee).select_related('detail')
        
        # Task statistics for employee
        task_counts = {
            'total': my_tasks.count(),
            'pending': my_tasks.filter(status='PENDING').count(),
            'in_progress': my_tasks.filter(status='IN_PROGRESS').count(),
            'completed': my_tasks.filter(status='COMPLETED').count(),
        }
        
        context = {
            'my_tasks': my_tasks,
            'task_counts': task_counts,
        }
    except Employee.DoesNotExist:
        # If user is not linked to Employee model
        context = {
            'my_tasks': [],
            'task_counts': {'total': 0, 'pending': 0, 'in_progress': 0, 'completed': 0},
            'message': 'Employee profile not found. Please contact administrator.'
        }
    
    return render(request, 'dashboard/employee_dashboard.html', context)

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
            return redirect('manager_dashboard')  # Redirect after successful submission
    return render(request,'task_form.html',{'task_form':task_form,'task_detail_form':task_detail_form})
@login_required
@permission_required('tasks.view_task', raise_exception=True)
def view_tasks(request):
    # Role-based task viewing
    user = request.user
    
    if user.groups.filter(name='Admin').exists() or user.is_superuser:
        # Admin can see all tasks
        projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
        tasks = Task.objects.all().select_related('detail')
        context_message = "All Tasks (Admin View)"
        
    elif user.groups.filter(name='Manager').exists():
        # Manager can see all tasks
        projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
        tasks = Task.objects.all().select_related('detail')
        context_message = "All Tasks (Manager View)"
        
    elif user.groups.filter(name='Employee').exists():
        # Employee can only see their assigned tasks
        try:
            employee = Employee.objects.get(user=user)
            projects = Project.objects.filter(task__assigned_to=employee).annotate(num_task=Count('task')).order_by('num_task').distinct()
            tasks = Task.objects.filter(assigned_to=employee).select_related('detail')
            context_message = "My Assigned Tasks"
        except Employee.DoesNotExist:
            projects = Project.objects.none()
            tasks = Task.objects.none()
            context_message = "Employee profile not found"
    else:
        # Default: no specific role
        projects = Project.objects.none()
        tasks = Task.objects.none()
        context_message = "No tasks available"
    
    context = {
        "projects": projects,
        "tasks": tasks,
        "context_message": context_message,
    }
    return render(request, 'show_tasks.html', context)

@login_required
@permission_required('tasks.delete_task', raise_exception=True)
def delete_task(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('manager-dashboard')
    return render(request, 'confirm_delete.html', {'task': task})