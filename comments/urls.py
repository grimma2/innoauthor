from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('projects/<int:project_id>/comment/', views.add_project_comment, name='add_project_comment'),
    path('newspost/<int:newspost_id>/comment/', views.add_newspost_comment, name='add_newspost_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
] 