from django.urls import path

from task_manager.statuses.views import (
    statuses_create,
    statuses_delete,
    statuses_edit,
    statuses_list,
)

app_name = 'statuses'

urlpatterns = [
    path('', statuses_list, name='statuses'),
    path('create/', statuses_create, name='statuses_create'),
    path('<int:pk>/update/', statuses_edit, name='statuses_edit'),
    path('<int:pk>/delete/', statuses_delete, name='statuses_delete'),
]

