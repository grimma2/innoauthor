from .models import ProjectInvitation

def pending_invitations(request):
    """
    Context processor that adds pending_invitations_count to the context.
    """
    context = {'pending_invitations_count': 0}
    
    if request.user.is_authenticated:
        context['pending_invitations_count'] = ProjectInvitation.objects.filter(
            invitee=request.user,
            status='pending'
        ).count()
        
    return context 
    
    
def projects_notifications(request):
    if not request.user.is_authenticated:
        return {}

    # Приглашения к пользователю
    pending_invitations = ProjectInvitation.objects.filter(
        invitee=request.user,
        status='pending'
    )

    # Заявки в проекты, где он автор
    project_applications = ProjectApplication.objects.filter(
        project__author=request.user
    )

    return {
        'pending_invitations_count': pending_invitations.count(),
        'project_applications_count': project_applications.count(),
        'projects_notifications_total': pending_invitations.count() + project_applications.count(),
    }