# Generated by Django 5.1.4 on 2025-01-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolbar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolbaritem',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='toolbar_images/'),
        ),
    ]