

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.db.models import Q, Count
from django.contrib import messages
from .forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date

#Class based view for reuse example
class GreetingView(View):
    greetings = "Hello, welcome to the Task Management System!"
    def get(self, request):
        return HttpResponse(self.greetings)
    
class HiGreetingView(GreetingView):
    greetings = "Hi there! This is a personalized greeting from HiGreetingView."   
# Create your views here.

def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()


class ManagerDashboardView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    @method_decorator(user_passes_test(is_manager, login_url='no_permission'), name='dispatch')
    def get(self, request):
        type = request.GET.get('type', 'all')
        counts = Task.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            completed=Count('id', filter=Q(status='COMPLETED')),
            inprogress=Count('id', filter=Q(status='IN_PROGRESS')),
        )
        base_Query = Task.objects.select_related('detail').prefetch_related('assigned_to')
        if type == 'pending':
            tasks = base_Query.filter(status='PENDING')
        elif type == 'completed':
            tasks = base_Query.filter(status='COMPLETED')
        elif type == 'inprogress':
            tasks = base_Query.filter(status='IN_PROGRESS')
        elif type == 'all':
            tasks = base_Query.all()
        context = self.get_context_data()
        context['tasks'] = tasks
        context['counts'] = counts
        return render(request, 'dashboard/manager_dashboard.html', context)
    def get_context_data(self, **kwargs):
        context = {}
        type = self.request.GET.get('type', 'all')
        counts = Task.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            completed=Count('id', filter=Q(status='COMPLETED')),
            inprogress=Count('id', filter=Q(status='IN_PROGRESS')),
        )
        base_Query = Task.objects.select_related('detail').prefetch_related('assigned_to')
        if type == 'pending':
            tasks = base_Query.filter(status='PENDING')
        elif type == 'completed':
            tasks = base_Query.filter(status='COMPLETED')
        elif type == 'inprogress':
            tasks = base_Query.filter(status='IN_PROGRESS')
        elif type == 'all':
            tasks = base_Query.all()
        context['tasks'] = tasks
        context['counts'] = counts
        return context

class EmployeeDashboardView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'
    @method_decorator(user_passes_test(is_employee, login_url='no_permission'), name='dispatch')
    def get(self, request):
        my_tasks = Task.objects.filter(assigned_to=request.user).select_related('detail')
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
        context = self.get_context_data()
        context['my_tasks'] = my_tasks
        context['task_counts'] = task_counts
        return render(request, 'dashboard/employee_dashboard.html', context)
    def get_context_data(self, **kwargs):
        context = {}
        my_tasks = Task.objects.filter(assigned_to=self.request.user).select_related('detail')
        task_counts = {
            'total': my_tasks.count(),
            'pending': my_tasks.filter(status='PENDING').count(),
            'in_progress': my_tasks.filter(status='IN_PROGRESS').count(),
            'completed': my_tasks.filter(status='COMPLETED').count(),
        }
        context['my_tasks'] = my_tasks
        context['task_counts'] = task_counts
        return context

# Class-based view for test
class TestView(View):
    def get(self, request):
        names = ["Mahmud", "Ahamed", "John", "Mr. X"]
        count = len(names)
        context = {
            "names": names,
            "age": 23,
            "count": count
        }
        return render(request, 'test.html', context)




class CreateTaskView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    login_url = 'login'
    redirect_field_name = 'next'
    permission_required = 'tasks.add_task'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        context['task_detail_form'] = TaskDetailModelForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        task_form = self.get_form()
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, 'Task created successfully!')
            return redirect('create-task')
        return self.render_to_response(self.get_context_data(form=task_form, task_detail_form=task_detail_form))



class UpdateTaskView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    login_url = 'login'
    redirect_field_name = 'next'
    permission_required = 'tasks.change_task'
    raise_exception = True
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        try:
            task_detail = task.detail
            task_detail_form = TaskDetailModelForm(instance=task_detail)
        except TaskDetail.DoesNotExist:
            task_detail_form = TaskDetailModelForm()
        context['task_form'] = self.get_form()
        context['task_detail_form'] = task_detail_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = self.get_form()
        try:
            task_detail = self.object.detail
            task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance=task_detail)
        except TaskDetail.DoesNotExist:
            task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('manager_dashboard')
        return self.render_to_response(self.get_context_data(form=task_form, task_detail_form=task_detail_form))


class ViewTasksView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Task
    template_name = 'show_tasks.html'
    context_object_name = 'tasks'
    login_url = 'login'
    redirect_field_name = 'next'
    permission_required = 'tasks.view_task'
    raise_exception = True

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            return Task.objects.all().select_related('detail')
        elif user.groups.filter(name='Manager').exists():
            return Task.objects.all().select_related('detail')
        elif user.groups.filter(name='Employee').exists():
            return Task.objects.filter(assigned_to=user).select_related('detail')
        else:
            return Task.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name='Admin').exists() or user.is_superuser:
            projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
            context_message = "All Tasks (Admin View)"
        elif user.groups.filter(name='Manager').exists():
            projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
            context_message = "All Tasks (Manager View)"
        elif user.groups.filter(name='Employee').exists():
            projects = Project.objects.filter(task__assigned_to=user).annotate(num_task=Count('task')).order_by('num_task').distinct()
            context_message = "My Assigned Tasks"
        else:
            projects = Project.objects.none()
            context_message = "No tasks available"
        context['projects'] = projects
        context['context_message'] = context_message
        return context



class ViewTaskDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    login_url = 'login'
    redirect_field_name = 'next'
    permission_required = 'tasks.view_task'
    raise_exception = True

    def get_queryset(self):
        return Task.objects.select_related('detail', 'project').prefetch_related('assigned_to__groups')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        team_members = []
        for user in task.assigned_to.all():
            groups = user.groups.all()
            role = groups[0].name if groups else 'Team Member'
            team_members.append({
                'user': user,
                'role': role,
                'groups': [g.name for g in groups],
            })
        context['team_members'] = team_members
        context['status_choices'] = Task.STATUS_CHOICES
        return context

    def post(self, request, id):
        task = Task.objects.select_related('detail', 'project').prefetch_related('assigned_to__groups').get(id=id)
        if request.user.has_perm('tasks.change_task') and 'task_status' in request.POST:
            new_status = request.POST.get('task_status')
            valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
            if new_status in valid_statuses:
                task.status = new_status
                task.is_completed = (new_status == 'COMPLETED')
                task.save()
                messages.success(request, f'Task status updated to {task.get_status_display()}!')
            return redirect('view_task_detail', id=id)
        else:
            messages.error(request, 'You do not have permission to change task status.')
        # Re-render the detail page with the same context as GET
        team_members = []
        for user in task.assigned_to.all():
            groups = user.groups.all()
            role = groups[0].name if groups else 'Team Member'
            team_members.append({
                'user': user,
                'role': role,
                'groups': [g.name for g in groups],
            })
        context = {
            'task': task,
            'team_members': team_members,
            'status_choices': Task.STATUS_CHOICES,
        }
        return render(request, 'task_detail.html', context)

class DeleteTaskView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    context_object_name = 'task'
    login_url = 'login'
    redirect_field_name = 'next'
    permission_required = 'tasks.delete_task'
    raise_exception = True
    pk_url_kwarg = 'id'
    success_url = '/tasks/manager-dashboard/'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)