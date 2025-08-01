# Generated by Django 5.2.4 on 2025-07-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='Тема')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
            ],
            options={
                'verbose_name': 'Сообщение контактов',
                'verbose_name_plural': 'Сообщения контактов',
                'ordering': ['-created_at'],
            },
        ),
    ]
