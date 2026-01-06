from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
class Task(models.Model):
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        default=1
    )
    assigned_to = models.ManyToManyField(Employee,related_name='tasks')
    title=models.CharField(max_length=200)
    description=models.TextField()
    due_date=models.DateField()
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

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
    assigned_to=models.CharField(max_length=100)
    priority=models.CharField(max_length=1, choices=PRIORITY_CHOICES,default=LOW)
    
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    