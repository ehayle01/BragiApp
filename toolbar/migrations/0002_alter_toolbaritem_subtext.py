# Generated by Django 5.1.4 on 2024-12-30 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolbar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolbaritem',
            name='subtext',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
