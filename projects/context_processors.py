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