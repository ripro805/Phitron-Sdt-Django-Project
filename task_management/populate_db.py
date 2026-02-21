
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
import django
django.setup()
from faker import Faker
import random

from tasks.models import Employee, Project, Task, TaskDetail
from users.models import CustomUser

# Function to populate the database


def populate_db():


        # Create Task Details (one per task)
        for task in tasks:
            if not hasattr(task, 'detail'):
                TaskDetail.objects.create(
                    task=task,
                    assigned_to=", ".join([
                        f"{user.first_name} {user.last_name}" for user in task.assigned_to.all()
                    ]),
                    priority=random.choice(['H', 'M', 'L']),
                    notes=fake.paragraph()
                )
        print("Populated TaskDetails for all tasks.")
        print("Database populated successfully!")
