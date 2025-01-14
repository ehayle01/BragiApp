# Generated by Django 5.1.4 on 2025-01-06 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_alter_comment_created_at'),
        ('notifications', '0001_initial'),
        ('posts', '0002_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.comment'),
        ),
        migrations.AddField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('like', 'Like'), ('follow', 'Follow'), ('comment', 'Comment'), ('reply', 'Reply')], max_length=20),
        ),
    ]
