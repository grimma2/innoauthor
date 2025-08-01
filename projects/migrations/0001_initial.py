# Generated by Django 5.2 on 2025-04-27 19:38

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('indexglav', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название проекта')),
                ('description', models.TextField(verbose_name='Описание проекта')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('project_photo', models.ImageField(blank=True, upload_to='static/img/projects', verbose_name='Фото проекта')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_projects', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('tags', models.ManyToManyField(related_name='projects', to='indexglav.tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
                'ordering': ['-create_datetime'],
            },
        ),
        migrations.CreateModel(
            name='ProjectInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitee_email', models.EmailField(max_length=254, verbose_name='Email приглашаемого')),
                ('token', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Ожидает ответа'), ('accepted', 'Принято'), ('declined', 'Отклонено')], default='pending', max_length=20)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('responded_at', models.DateTimeField(blank=True, null=True)),
                ('invitee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='projects.project')),
            ],
            options={
                'verbose_name': 'Приглашение в проект',
                'verbose_name_plural': 'Приглашения в проекты',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ManyToManyField(related_name='projects', through='projects.ProjectInvitation', to=settings.AUTH_USER_MODEL, verbose_name='Команда'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название задачи')),
                ('description', models.TextField(blank=True, verbose_name='Описание задачи')),
                ('status', models.CharField(choices=[('pending', 'Ожидает выполнения'), ('in_progress', 'В процессе'), ('completed', 'Выполнено')], default='pending', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Срок выполнения')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ['status', 'deadline', '-created_at'],
            },
        ),
    ]
