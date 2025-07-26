from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class RegisterUserForm(UserCreationForm):
    patronymic = forms.CharField(max_length=30, required=False, label='Отчество')
    phone = forms.CharField(max_length=17, required=True, label='Телефон')
    consent = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных',
        error_messages={'required': 'Вы должны согласиться с обработкой персональных данных'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'phone', 'password1', 'password2', 'consent')
        labels = {
            'email': 'Email',
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.patronymic = self.cleaned_data['patronymic']
        user.phone = self.cleaned_data['phone']
        user.is_active = False  # User needs to verify email to become active
        
        if commit:
            user.save()
            # Generate verification token
            user.generate_verification_token()
            
        return user
