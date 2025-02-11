# Generated by Django 5.1.4 on 2025-01-16 18:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='group_cover_images/')),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='group_members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_add_group', 'Can add a new group'), ('can_edit_group', 'Can edit a group'), ('can_delete_group', 'Can delete a group')],
            },
        ),
    ]
