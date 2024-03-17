from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .forms import LoginForm

app_name = 'account'


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('signin/', LoginView.as_view(template_name='signin.html', form_class=LoginForm), name='signin'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout')
]
