from django.db.models.signals import post_save, pre_save,post_delete,m2m_changed
from django.dispatch import receiver 
from django.core.mail import send_mail
from tasks.models import Task
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