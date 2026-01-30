from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
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
        on_delete=models.CASCADE,
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
from django.db.models.signals import post_delete

@receiver(pre_save, sender=Task)
def notify_tasks_creation(sender, instance, **kwargs):
    if instance._state.adding:  # Check if the instance is being created
        print(f"New Task Created: {instance.title}")    
        instance.is_completed =True

@receiver(post_delete, sender=Task)
def notify_task_deletion(sender, instance, **kwargs):
    print(f"Task Deleted: {instance.title}")