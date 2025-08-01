# Generated by Django 5.2 on 2025-04-27 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название тега')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Newspost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namepost', models.CharField(max_length=100, verbose_name='Название поста')),
                ('humanpost', models.CharField(max_length=100, verbose_name='От кого новость')),
                ('soderjanie', models.TextField(verbose_name='Содержание поста')),
                ('postdate', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время поста')),
                ('post_photo', models.ImageField(blank=True, upload_to='static/img', verbose_name='Фото')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='URL')),
                ('tags', models.ManyToManyField(related_name='news_posts', to='indexglav.tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-postdate'],
            },
        ),
    ]
