from django.contrib import admin
from django.urls import path
from task_manager.views import (
    index, labels, statuses_create, labels_create, labels_edit,
    labels_delete, tasks, tasks_create, tasks_detail, statuses,
    tasks_delete, tasks_edit, users, users_edit, users_delete,
    users_create, statuses_delete, statuses_edit, LoginView, LogoutView
)

urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),
    path('users/', users, name='users'),
    path('users/<int:pk>/update/', users_edit, name='users_edit'),
    path('users/<int:pk>/delete/', users_delete, name='users_delete'),
    path('users/create/', users_create, name='create'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('statuses/', statuses, name='statuses'),
    path('statuses/create/', statuses_create, name='statuses_create'),
    path('statuses/<int:pk>/update/', statuses_edit, name='statuses_edit'),
    path('statuses/<int:pk>/delete/', statuses_delete, name='statuses_delete'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/create/', tasks_create, name='tasks_create'),
    path('tasks/<int:pk>/', tasks_detail, name='tasks_detail'),
    path('tasks/<int:pk>/update/', tasks_edit, name='tasks_edit'),
    path('tasks/<int:pk>/delete/', tasks_delete, name='tasks_delete'),
    path('labels/', labels, name='labels'),
    path('labels/create/', labels_create, name='labels_create'),
    path('labels/<int:pk>/update/', labels_edit, name='labels_edit'),
    path('labels/<int:pk>/delete/', labels_delete, name='labels_delete'),
]
