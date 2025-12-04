from django.urls import path
from task_manager.users.views import users_list, users_edit, users_delete, users_create

app_name = 'users'

urlpatterns = [
    path('', users_list, name='users'),
    path('<int:pk>/update/', users_edit, name='users_edit'),
    path('<int:pk>/delete/', users_delete, name='users_delete'),
    path('create/', users_create, name='create'),
]

