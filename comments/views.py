from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm
from .models import Comment
from projects.models import Project
from indexglav.models import Newspost

@login_required
def add_project_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.content_object = project
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
            return redirect('projects:project_detail', project_slug=project.slug)
    
    return redirect('projects:project_detail', project_slug=project.slug)

@login_required
def add_newspost_comment(request, newspost_id):
    newspost = get_object_or_404(Newspost, id=newspost_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.content_object = newspost
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
            return redirect('indexglav:news_detail', slug=newspost.slug)
    
    return redirect('indexglav:news_detail', slug=newspost.slug)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Get the content object and determine where to redirect
    content_object = comment.content_object
    
    # Check if user is author of comment or admin
    if request.user == comment.author or request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            comment.delete()
            messages.success(request, 'Комментарий удален.')
    else:
        messages.error(request, 'У вас нет прав для удаления этого комментария.')
    
    # Redirect back to the appropriate page
    if isinstance(content_object, Project):
        return redirect('projects:project_detail', project_slug=content_object.slug)
    elif isinstance(content_object, Newspost):
        return redirect('indexglav:news_detail', slug=content_object.slug)
    else:
        # Fallback redirect
        return redirect('indexglav:indexglav') 