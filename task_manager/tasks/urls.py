from django.urls import path
from task_manager.tasks.views import (
    tasks_list, tasks_create, tasks_detail, tasks_edit, tasks_delete
)

app_name = 'tasks'

urlpatterns = [
    path('', tasks_list, name='tasks'),
    path('create/', tasks_create, name='tasks_create'),
    path('<int:pk>/delete/', tasks_delete, name='tasks_delete'),
    path('<int:pk>/update/', tasks_edit, name='tasks_edit'),
    path('<int:pk>/', tasks_detail, name='tasks_detail'),
]

