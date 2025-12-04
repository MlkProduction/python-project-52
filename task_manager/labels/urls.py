from django.urls import path

from task_manager.labels.views import (
    labels_create,
    labels_delete,
    labels_edit,
    labels_list,
)

app_name = 'labels'

urlpatterns = [
    path('', labels_list, name='labels'),
    path('create/', labels_create, name='labels_create'),
    path('<int:pk>/update/', labels_edit, name='labels_edit'),
    path('<int:pk>/delete/', labels_delete, name='labels_delete'),
]

