# Generated by Django 5.1.4 on 2025-01-16 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToolbarAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('alt_text', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='toolbar_images/')),
                ('url', models.URLField(blank=True, null=True)),
                ('visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ToolbarItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.FileField(blank=True, null=True, upload_to='toolbar_images/')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.IntegerField(default=0)),
                ('visible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='UsersItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.FileField(blank=True, null=True, upload_to='toolbar_images/')),
                ('description', models.TextField(blank=True, null=True)),
                ('visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserChildItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.FileField(blank=True, null=True, upload_to='toolbar_images/')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('visible', models.BooleanField(default=True)),
                ('list_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='toolbar.usersitem')),
            ],
        ),
    ]
