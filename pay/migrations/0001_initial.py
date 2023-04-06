# Generated by Django 4.1.7 on 2023-03-29 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('startValidaity', models.DateField()),
                ('endValidaity', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberVideos', models.IntegerField()),
                ('videoTemplates', models.IntegerField()),
                ('watermark', models.BooleanField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pay.plan')),
            ],
        ),
    ]
