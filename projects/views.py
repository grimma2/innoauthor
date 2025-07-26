from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Project, ProjectInvitation, Task
from indexglav.models import Tag
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import slugify
import re
from transliterate import translit
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment
from .forms import InvitationForm, TaskForm
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import PageNotAnInteger, EmptyPage

User = get_user_model()

def cyrillic_slugify(s):
    """
    Переводит строку с кириллицей в латиницу и применяет slugify
    """
    # Транслитерация из кириллицы в латиницу
    if s:
        s = translit(s, 'ru', reversed=True)
        # Применение стандартного slugify
        s = slugify(s)
        return s
    return ''

def projects(request):
    """Отображение списка проектов"""
    # Get all tags for filtering
    tags = Tag.objects.all()
    
    # Handle tag filtering
    current_tag = request.GET.get('tag')
    if current_tag:
        projects_list = Project.objects.filter(tags__slug=current_tag, is_private=False)
    else:
        projects_list = Project.objects.filter(is_private=False)
    
    # Handle status filtering
    current_status = request.GET.get('status')
    if current_status:
        projects_list = projects_list.filter(status=current_status)
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        projects_list = projects_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(projects_list, 10)  # Show 10 projects per page
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    return render(request, 'projects.html', {
        'projects': projects,
        'tags': tags,
        'current_tag': current_tag,
        'current_status': current_status,
        'search_query': search_query,
        'status_choices': Project.STATUS_CHOICES,
        'is_paginated': paginator.num_pages > 1,
        'paginator': paginator
    })

@login_required
def my_projects(request):
    # Get projects where user is author
    authored_projects = Project.objects.filter(author=request.user)
    
    # Get projects where user is a team member
    team_projects = Project.objects.filter(
        invitations__invitee=request.user,
        invitations__status='accepted'
    )
    
    # Get pending invitations
    pending_invitations = ProjectInvitation.objects.filter(
        invitee=request.user,
        status='pending'
    )
    
    # Combine all projects without duplicates
    projects_list = (authored_projects | team_projects).distinct()
    
    return render(request, 'my_projects.html', {
        'projects': projects_list,
        'pending_invitations': pending_invitations,
    })

@login_required
def create_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        project_photo = request.FILES.get('project_photo')
        tag_ids = request.POST.getlist('tags')
        is_private = bool(request.POST.get('is_private'))
        
        # Проверяем уникальность имени проекта
        if Project.objects.filter(title=title).exists():
            messages.error(request, 'Проект с таким названием уже существует. Пожалуйста, выберите другое название.')
            tags = Tag.objects.all()
            return render(request, 'create_project.html', {
                'tags': tags,
                'form_data': {
                    'title': title,
                    'description': description,
                    'tag_ids': tag_ids
                }
            })
        
        if title and description:
            project = Project.objects.create(
                title=title,
                description=description,
                author=request.user,
                project_photo=project_photo,
                slug=cyrillic_slugify(title),
                is_private=is_private
            )
            project.tags.set(tag_ids)
            print(f'project.slug: {project.slug}')
            messages.success(request, 'Проект успешно создан!')
            return redirect('projects:project_detail', project_slug=project.slug)
            
    tags = Tag.objects.all()
    return render(request, 'create_project.html', {'tags': tags})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user is author or admin
    if request.user == project.author or request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            try:
                # Manually delete related records that might cause foreign key constraint issues
                from django.db import connection
                
                with connection.cursor() as cursor:
                    # Delete any records from projects_reportproject table if it exists
                    try:
                        cursor.execute("DELETE FROM projects_reportproject WHERE project_id = %s", [project_id])
                    except Exception:
                        # Table might not exist, ignore the error
                        pass
                
                # Now delete the project (this will cascade delete related records with CASCADE)
                project.delete()
                messages.success(request, 'Проект успешно удален')
                return redirect('projects:my_projects')
            except Exception as e:
                messages.error(request, f'Ошибка при удалении проекта: {str(e)}')
                return redirect('projects:my_projects')
    else:
        messages.error(request, 'У вас нет прав для удаления этого проекта')
    
    return redirect('projects:my_projects')

def liderplatform1(request):
    return render(request, 'glavfooter/liderplatform.html')
    
def workshop1(request):
    return render(request, 'glavfooter/workshop.html')

def documents1(request):
    return render(request, 'glavfooter/documents.html')

def shop1(request):
    return render(request, 'glavfooter/shop.html')

def service1(request):
    return render(request, 'glavfooter/service.html')

def contact1(request):
    return render(request, 'glavfooter/contact.html')

# Добавляем представление для детального просмотра проекта
def project_detail(request, project_slug):
    """Отображение детальной страницы проекта"""
    project = get_object_or_404(Project, slug=project_slug)
    
    # Get comments for this project
    content_type = ContentType.objects.get_for_model(Project)
    comments = Comment.objects.filter(content_type=content_type, object_id=project.id)
    
    # Check permissions
    is_owner = request.user == project.author
    
    # Get team members
    team_members = User.objects.filter(
        Q(invitations__project=project, invitations__status='accepted') | 
        Q(id=project.author.id)
    )
    
    is_team_member = request.user in team_members
    
    # Get tasks for this project
    tasks = None
    task_form = None
    if is_team_member or is_owner:
        tasks = Task.objects.filter(project=project)
        
        # Prepare task form if user is the owner
        if is_owner:
            task_form = TaskForm(project=project)
    
    # Prepare invitation form if user is the owner
    invitation_form = None
    if is_owner:
        invitation_form = InvitationForm()
    
    # Prepare comment form
    comment_form = CommentForm()
    comment_form_action = f'/comments/projects/{project.id}/comment/'
    
    context = {
        'project': project,
        'comments': comments,
        'comment_form': comment_form,
        'comment_form_action': comment_form_action,
        'is_owner': is_owner,
        'is_team_member': is_team_member,
        'team_members': team_members,
        'invitation_form': invitation_form,
        'tasks': tasks,
        'task_form': task_form,
    }
    
    return render(request, 'project_detail.html', context)

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user is author or admin
    if not (request.user == project.author or request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'У вас нет прав для редактирования этого проекта')
        return redirect('projects:project_detail', project_slug=project.slug)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        project_photo = request.FILES.get('project_photo')
        tag_ids = request.POST.getlist('tags')
        
        # Check if title exists and is different from current project
        if title and title != project.title and Project.objects.filter(title=title).exists():
            messages.error(request, 'Проект с таким названием уже существует. Пожалуйста, выберите другое название.')
            tags = Tag.objects.all()
            return render(request, 'edit_project.html', {
                'project': project,
                'tags': tags,
            })
        
        if title:
            project.title = title
        
        if description:
            project.description = description
        
        if project_photo:
            project.project_photo = project_photo
        
        # Only update slug if title changed
        if title and title != project.title:
            project.slug = cyrillic_slugify(title)
        
        project.save()
        
        if tag_ids:
            project.tags.set(tag_ids)
        
        messages.success(request, 'Проект успешно обновлен!')
        return redirect('projects:project_detail', project_slug=project.slug)
    
    tags = Tag.objects.all()
    return render(request, 'edit_project.html', {
        'project': project,
        'tags': tags,
    })

@login_required
def invite_member(request, project_id):
    """Send invitation to a user to join the project"""
    project = get_object_or_404(Project, id=project_id)
    
    # Only the project owner can send invitations
    if request.user != project.author:
        messages.error(request, 'Только автор проекта может приглашать участников.')
        return redirect('projects:project_detail', project_slug=project.slug)
    
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.project = project
            
            # Check if email already invited to this project
            if ProjectInvitation.objects.filter(
                project=project, 
                invitee_email=invitation.invitee_email, 
                status='pending'
            ).exists():
                messages.warning(request, f'Пользователь с email {invitation.invitee_email} уже приглашен в этот проект.')
                return redirect('projects:project_detail', project_slug=project.slug)
            
            # Check if user with this email already exists
            try:
                user = User.objects.get(email=invitation.invitee_email)
                invitation.invitee = user
                
                # Check if user is already a team member or the author
                if ProjectInvitation.objects.filter(
                    project=project, 
                    invitee=user, 
                    status='accepted'
                ).exists() or user == project.author:
                    messages.warning(request, f'Пользователь {user.username} уже является участником проекта.')
                    return redirect('projects:project_detail', project_slug=project.slug)
                    
            except User.DoesNotExist:
                messages.warning(request, f'Пользователя с таким email не существует.')
                return redirect('projects:project_detail', project_slug=project.slug)

            invitation.save()
            
            # Generate invitation URL
            invite_url = f"{request.scheme}://{request.get_host()}/projects/invitations/accept/{invitation.token}"
            
            # Prepare email context
            email_context = {
                'project': project,
                'inviter': request.user,
                'invite_url': invite_url,
            }
            
            # Render email templates
            html_message = render_to_string('emails/invite.html', email_context)
            plain_message = strip_tags(html_message)
            
            # Send email
            try:
                send_mail(
                    subject=f'Приглашение в проект "{project.title}" на InnAuthor',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[invitation.invitee_email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f'Ошибка при отправке приглашения, возможно такого email не существует.')
                return redirect('projects:project_detail', project_slug=project.slug)

            messages.success(request, f'Приглашение отправлено на {invitation.invitee_email}')
            return redirect('projects:project_detail', project_slug=project.slug)
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('projects:project_detail', project_slug=project.slug)

@login_required
def accept_invitation(request, token):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Store the token in session and redirect to login
        request.session['invitation_token'] = token
        request.session['invitation_action'] = 'accept'
        messages.info(request, 'Пожалуйста, войдите в систему, чтобы принять приглашение.')
        return redirect('users:login')
        
    invitation = get_object_or_404(ProjectInvitation, token=token, status='pending')
    
    # Ensure the invitation is for the logged-in user
    if invitation.invitee and invitation.invitee != request.user:
        messages.error(request, 'Это приглашение предназначено для другого пользователя.')
        return redirect('projects:my_projects')
    
    # If invitee is not set (email invitation), set it now
    if not invitation.invitee and invitation.invitee_email == request.user.email:
        invitation.invitee = request.user
    elif not invitation.invitee and invitation.invitee_email != request.user.email:
        messages.error(request, 'Это приглашение предназначено для другого email адреса.')
        return redirect('projects:my_projects')
    
    # Accept invitation
    invitation.status = 'accepted'
    invitation.responded_at = timezone.now()
    invitation.save()
    
    messages.success(request, f'Вы успешно присоединились к проекту "{invitation.project.title}".')
    return redirect('projects:project_detail', project_slug=invitation.project.slug)

@login_required
def decline_invitation(request, token):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Store the token in session and redirect to login
        request.session['invitation_token'] = token
        request.session['invitation_action'] = 'decline'
        messages.info(request, 'Пожалуйста, войдите в систему, чтобы отклонить приглашение.')
        return redirect('users:login')
        
    invitation = get_object_or_404(ProjectInvitation, token=token, status='pending')
    
    # Ensure the invitation is for the logged-in user
    if invitation.invitee and invitation.invitee != request.user:
        messages.error(request, 'Это приглашение предназначено для другого пользователя.')
        return redirect('projects:my_projects')
    
    # If invitee is not set (email invitation), check if it matches current user's email
    if not invitation.invitee and invitation.invitee_email != request.user.email:
        messages.error(request, 'Это приглашение предназначено для другого email адреса.')
        return redirect('projects:my_projects')
    
    # Decline invitation
    invitation.status = 'declined'
    invitation.responded_at = timezone.now()
    invitation.save()
    
    messages.info(request, f'Вы отклонили приглашение в проект "{invitation.project.title}".')
    return redirect('projects:my_projects')

def verify_invitation(request):
    token = request.GET.get('token')
    if not token:
        messages.error(request, 'Неверная ссылка приглашения.')
        return redirect('indexglav:indexglav')
    
    invitation = get_object_or_404(ProjectInvitation, token=token, status='pending')
    
    # If user is not logged in, redirect to login
    if not request.user.is_authenticated:
        messages.info(request, 'Пожалуйста, войдите в систему, чтобы принять приглашение.')
        return redirect('users:login')
    
    # If invitation has an invitee set, check if it matches current user
    if invitation.invitee and invitation.invitee != request.user:
        messages.error(request, 'Это приглашение предназначено для другого пользователя.')
        return redirect('indexglav:indexglav')
    
    # If invitation is by email, check if current user's email matches
    if not invitation.invitee and invitation.invitee_email != request.user.email:
        messages.error(request, 'Это приглашение предназначено для другого email адреса.')
        return redirect('indexglav:indexglav')
    
    return render(request, 'verify_invitation.html', {
        'invitation': invitation,
    })

@login_required
def add_task(request, project_id):
    """Add a new task to a project"""
    project = get_object_or_404(Project, id=project_id)
    
    # Only project owner can add tasks
    if request.user != project.author:
        messages.error(request, 'Только владелец проекта может добавлять задачи.')
        return redirect('projects:project_detail', project_slug=project.slug)
    
    if request.method == 'POST':
        form = TaskForm(project, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            
            messages.success(request, 'Задача успешно добавлена.')
            
            # If task was assigned to someone, notify them
            if task.assigned_to and task.assigned_to != request.user:
                # This would typically send an email notification
                pass
                
            return redirect('projects:project_detail', project_slug=project.slug)
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('projects:project_detail', project_slug=project.slug)

@login_required
def update_task(request, task_id):
    """Update an existing task"""
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    
    # Only project owner or task assignee can update
    if request.user != project.author and request.user != task.assigned_to:
        messages.error(request, 'У вас нет прав для изменения этой задачи.')
        return redirect('projects:project_detail', project_slug=project.slug)
    
    if request.method == 'POST':
        # Project owner can edit all fields, assignee can only update status
        if request.user == project.author:
            form = TaskForm(project, request.POST, instance=task)
        else:
            form = TaskForm(project, request.POST, instance=task)
            form.fields.pop('title')
            form.fields.pop('description')
            form.fields.pop('assigned_to')
            form.fields.pop('deadline')
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена.')
            return redirect('projects:project_detail', project_slug=project.slug)
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('projects:project_detail', project_slug=project.slug)

@login_required
def delete_task(request, task_id):
    """Delete a task"""
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    
    # Only project owner can delete tasks
    if request.user != project.author:
        messages.error(request, 'Только владелец проекта может удалять задачи.')
        return redirect('projects:project_detail', project_slug=project.slug)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена.')
    
    return redirect('projects:project_detail', project_slug=project.slug)