# Generated by Django 4.1.7 on 2023-03-10 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('top_text', models.CharField(max_length=200)),
                ('bottom_text', models.CharField(max_length=200)),
                ('audio', models.FileField(upload_to='media/uploads/audio/')),
                ('images', models.ManyToManyField(blank=True, null=True, to='video.imagelist')),
            ],
        ),
    ]
