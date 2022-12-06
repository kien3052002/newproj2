from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        authentication_form=UserLoginForm, template_name="registration/login.html"), name='login'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.accounts_register, name='register')
]
