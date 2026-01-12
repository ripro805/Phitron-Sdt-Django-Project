from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, test, create_task, view_tasks, update_task

urlpatterns = [
    path('manager-dashboard/', manager_dashboard,name='manager-dashboard'),
    path('user-dashboard/', user_dashboard),
    path('test/', test),
    path('create-task/', create_task,name='create-task'),
    path('view-tasks/', view_tasks),
    path('update-task/<int:id>/', update_task, name='update-task'),
]