# Generated by Django 4.1.7 on 2023-04-01 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='validaity',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]