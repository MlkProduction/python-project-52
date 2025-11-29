"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from task_manager.models import Labels, Users
from task_manager.views import index, labels, statuses_create, labels_create, labels_edit, labels_delete, tasks, tasks_create, statuses, tasks_delete, tasks_edit, users, users_edit, users_delete, users_create, statuses_delete, statuses_edit
from django.contrib.auth import views as auth_views





urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),
    path('users/', users, name='users'),
    path('users/<int:pk>/update/', users_edit, name='users_edit'), 
    path('users/<int:pk>/delete/', users_delete, name='users_delete'), 
    path('users/create/', users_create, name='create'), 
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('statuses/', statuses, name='statuses'),    
    path('statuses/create/', statuses_create, name='statuses_create'),
    path('statuses/<int:pk>/update/', statuses_edit, name='statuses_edit'), 
    path('statuses/<int:pk>/delete/', statuses_delete, name='statuses_delete'), 
    path('tasks/', tasks, name='tasks/'),    
    path('tasks/create/', tasks_create, name='tasks_create'),
    path('tasks/<int:pk>/update/', tasks_edit, name='tasks_edit'), 
    path('tasks/<int:pk>/delete/', tasks_delete, name='tasks_delete'),     
    path('labels/', labels, name='labels'),   
    path('labels/create/', labels_create, name='labels_create'),
    path('labels/<int:pk>/update/', labels_edit, name='labels_edit'), 
    path('labels/<int:pk>/delete/', labels_delete, name='labels_delete'),  
]
