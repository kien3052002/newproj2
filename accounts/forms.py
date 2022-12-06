from django.shortcuts import redirect
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control login-form-control', 'placeholder': 'Tài khoản', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control login-form-control',
            'placeholder': 'Mật khẩu',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):

    username = forms.CharField(
        label='Tài khoản (4-50 kí tự)', min_length=4, max_length=50)
    email = forms.EmailField(max_length=100, error_messages={
                             'invalid': '*Email đã đăng kí', })
    password = forms.CharField(
        label='Mật khẩu', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Nhập lại mật khẩu', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("*Tên tài khoản đã tồn tại")
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('*Mật khẩu không trùng khớp')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('*Email đã đăng kí')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3 register-form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3 register-form-control', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control register-form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control register-form-control', 'placeholder': 'Repeat Password'})
