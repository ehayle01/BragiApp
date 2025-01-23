# Generated by Django 5.1.4 on 2025-01-23 06:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_category_post_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='post_images/additional/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='posts.post')),
            ],
        ),
    ]
