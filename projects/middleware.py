from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class InvitationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if this is a login redirect with invitation token
        if request.path.startswith('/users/login/') and 'next' in request.GET:
            next_url = request.GET['next']
            if '/projects/invitations/accept/' in next_url or '/projects/invitations/decline/' in next_url:
                # Extract token from the next URL
                token = next_url.split('/')[-1]
                action = 'accept' if 'accept' in next_url else 'decline'
                
                # Store in session
                request.session['invitation_token'] = token
                request.session['invitation_action'] = action
                
                # Add message
                messages.info(request, 'Пожалуйста, войдите в систему, чтобы принять приглашение.')
        
        response = self.get_response(request)
        return response 