from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserLoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User


@login_required
def profile(request, id):
    user_id = id
    requested_user = User.objects.filter(id=user_id)[0]
    return render(request, 'accounts/profile.html', {'requested_user': requested_user})


def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = True
            user.save()
            return redirect("accounts:login")
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})
