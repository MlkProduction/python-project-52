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
from task_manager.models import Users
from task_manager.views import index, users, users_edit, users_delete, users_create
from django.contrib.auth import views as auth_views





urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),
    path('users/', users, name='users'),
    path('users/<int:pk>/edit', users_edit, name='users_edit'), 
    path('users/<int:pk>/delete', users_delete, name='users_delete'), 
    path('users/create/', users_create, name='create'), 
    path("login/", auth_views.LoginView.as_view(), name="login"),
]
