from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.urls import reverse, reverse_lazy
from .forms import LoginUserForm, UserProfileForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    extra_context = {'title': 'Авторизация'}
    
    def get_success_url(self):
        # Default redirect to the homepage
        return reverse_lazy('indexglav:indexglav')
        
    def form_valid(self, form):
        """Log in the user and then check for invitation tokens."""
        response = super().form_valid(form)
        return response

def verify_email(request, token):
    """Handle email verification using the token."""
    user = get_object_or_404(User, verification_token=token)
    
    # Check if token is expired (48 hours)
    token_expiry = timedelta(hours=48)
    if user.token_created_at + token_expiry < timezone.now():
        messages.error(request, 'Ссылка для подтверждения устарела. Пожалуйста, запросите новую.')
        user.generate_verification_token()  # Generate new token
        # Here you would typically send a new verification email
        return redirect('users:login')
    
    # Verify email and activate user
    user.verify_email()
    user.is_active = True
    user.save()
    
    messages.success(request, 'Email успешно подтвержден! Теперь вы можете войти в систему.')
    return redirect('users:login')

@login_required
def profile(request):
    return render(request, 'profile/profile.html', {
        'user': request.user,
        'active_tab': 'general'
    })

@login_required
def profile_general(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен")
            return redirect('users:profile_general')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile/general.html', {
        'form': form,
        'active_tab': 'general'
    })

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'profile/security.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:profile_security')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'security'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменен")
        return super().form_valid(form)

@login_required
def profile_security(request):
    return UserPasswordChangeView.as_view()(request)

def public_profile(request, username):
    """Display public profile of a user."""
    user = get_object_or_404(User, username=username)
    
    # Get user's projects
    # Since we can't import Projects directly due to circular imports, 
    # we'll fetch the projects in the template
    
    return render(request, 'profile/public_profile.html', {
        'profile_user': user
    })

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return render(request, 'accounts/register.html')
        
        user = User.objects.create_user(
            email=email, username=username,
            first_name=first_name, last_name=last_name,
            password=password
        )
        user.is_active = False  # Блокируем до подтверждения
        user.generate_verification_token()
        user.save()
        
        # Формируем verification_url ПРАВИЛЬНО
        verification_url = request.scheme + '://' + request.get_host() + '/verify/' + str(user.verification_token)
        
        subject = 'Подтвердите email - ИнноАвтор'
        html_message = render_to_string('emails/verify_email.html', {
            'user': user,
            'verification_url': verification_url
        })
        send_mail(subject, strip_tags(html_message), 'innoauthor@mail.ru', [email], html_message=html_message, fail_silently=False)
        
        messages.success(request, 'Регистрация прошла успешно! Проверьте почту для подтверждения.')
        return redirect('users:login')
    
    return render(request, 'accounts/register.html')
