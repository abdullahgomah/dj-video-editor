# Generated by Django 4.1.7 on 2023-04-17 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0013_plan_videos_per_months'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='numberVideos',
        ),
    ]
