from django import forms
from .models import ProjectInvitation, Task
from django.contrib.auth import get_user_model

User = get_user_model()

class InvitationForm(forms.ModelForm):
    class Meta:
        model = ProjectInvitation
        fields = ('invitee_email',)
        widgets = {
            'invitee_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email участника'}),
        }
        labels = {
            'invitee_email': 'Email',
        }
        help_texts = {
            'invitee_email': 'Введите email пользователя, которого хотите пригласить в проект',
        }

class TaskForm(forms.ModelForm):
    title = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'assigned_to', 'deadline')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название задачи'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание задачи'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, project, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        
        # Only show team members and project creator in assigned_to dropdown
        team_members = User.objects.filter(
            invitations__project=project,
            invitations__status='accepted'
        )
        
        # Add project creator
        team_members = (team_members | User.objects.filter(pk=project.author.pk)).distinct()
        
        self.fields['assigned_to'].queryset = team_members 