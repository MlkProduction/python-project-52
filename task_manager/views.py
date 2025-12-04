from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView
)


def index(request):
    return render(request, "index.html", {"who": "World"})


class LoginView(BaseLoginView):
    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)


class LogoutView(BaseLogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
