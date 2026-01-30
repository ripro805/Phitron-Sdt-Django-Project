from django.db import models
from django.db.models.signals import post_save, pre_save,post_delete,m2m_changed
from django.dispatch import receiver 
from django.core.mail import send_mail
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name
class Task(models.Model): 
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        default=1
    )
    assigned_to = models.ManyToManyField(Employee,related_name='tasks')
    title=models.CharField(max_length=200)
    description=models.TextField()
    due_date=models.DateField()
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="PENDING")
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class TaskDetail(models.Model):
    HIGH='H'
    MEDIUM='M'
    LOW='L'
    PRIORITY_CHOICES = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )
    task=models.OneToOneField(
        Task, 
        on_delete=models.DO_NOTHING,
        related_name='detail'
       )
    
    priority=models.CharField(max_length=1, choices=PRIORITY_CHOICES,default=LOW)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Details form Task {self.task.title}"
    
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    
    
    def __str__(self):
        return self.name
    
#signals

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_tasks_creation(sender, instance,action, **kwargs):
    if action=='post_add':
        employees = instance.assigned_to.all()
        for employee in employees:
            print(f"Notification: Task '{instance.title}' has been assigned to {employee.name} ({employee.email})")
            
        send_mail(
            subject=f"New Task Assigned: {instance.title}",
            message=f"You have been assigned a new task: {instance.title}\nDescription: {instance.description}\nDue Date: {instance.due_date}",
            from_email="rifatrizviofficial001@gmail.com",
            recipient_list=[employee.email for employee in employees],
            fail_silently=False,
        )
        
        
@receiver(post_delete, sender=Task)
def notify_task_deletion(sender, instance, **kwargs):
    detail = getattr(instance, 'detail', None)
    if detail:
        print(f"TaskDetail for '{instance.title}' also deleted.")
    print(f"Task Deleted: {instance.title}")