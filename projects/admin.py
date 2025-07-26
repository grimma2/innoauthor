from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Project, ProjectInvitation, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_private', 'create_datetime', 'slug')
    list_filter = ('is_private', 'tags', 'create_datetime', 'author')
    search_fields = ('title', 'description', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.project_photo:
            return mark_safe(f'<img src="{obj.project_photo.url}" style="max-width: 100px; max-height: 100px;">')
        return 'No image'

    image_preview.short_description = 'Preview'

@admin.register(ProjectInvitation)
class ProjectInvitationAdmin(admin.ModelAdmin):
    list_display = ('project', 'invitee_email', 'invitee', 'status', 'sent_at')
    list_filter = ('status', 'sent_at')
    search_fields = ('project__title', 'invitee_email', 'invitee__username')
    readonly_fields = ('token',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'created_by', 'assigned_to', 'created_at', 'deadline')
    list_filter = ('status', 'project', 'created_at', 'deadline')
    search_fields = ('title', 'description', 'project__title')
    raw_id_fields = ('project', 'created_by', 'assigned_to')
    date_hierarchy = 'created_at'
