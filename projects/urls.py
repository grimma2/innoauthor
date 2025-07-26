from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path('', views.projects, name='projects'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('create/', views.create_project, name='create_project'),
    path('project/<slug:project_slug>/', views.project_detail, name='project_detail'),
    path('edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('liderplatform1/', views.liderplatform1, name='liderplatform1'),
    path('workshop1/', views.workshop1, name='workshop1'),
    path('documents1/', views.documents1, name='documents1'),
    path('shop1/', views.shop1, name='shop1'),
    path('service1/', views.service1, name='service1'),
    path('contact1/', views.contact1, name='contact1'),
    
    # Invitation URLs
    path('project/<int:project_id>/invite/', views.invite_member, name='invite_member'),
    path('invitations/accept/<str:token>/', views.accept_invitation, name='accept_invitation'),
    path('invitations/decline/<str:token>/', views.decline_invitation, name='decline_invitation'),
    path('invitations/verify/', views.verify_invitation, name='verify_invitation'),
    
    # Task URLs
    path('project/<int:project_id>/tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]