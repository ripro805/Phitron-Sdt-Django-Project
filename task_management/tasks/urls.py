from django.urls import path
from tasks.views import show_tasks

urlpatterns=[
    path('show-tasks/',show_tasks)
]