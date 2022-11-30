from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'section':'profile'})
    

def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})
