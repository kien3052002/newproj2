from django.shortcuts import render, redirect
from .forms import RegistrationForm


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
