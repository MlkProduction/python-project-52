from django.contrib import admin
from django.urls import path, include
from task_manager.views import index, LoginView, LogoutView

urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('users/', include('users.urls')),
    path('statuses/', include('statuses.urls')),
    path('tasks/', include('tasks.urls')),
    path('labels/', include('labels.urls')),
]
