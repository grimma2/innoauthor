from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'password']

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    patronymic = forms.CharField(
        required=False,
        label='Отчество',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    about = forms.CharField(
        required=False,
        label='О себе',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    avatar = forms.ImageField(
        required=False,
        label='Фото профиля',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'about', 'avatar']