# Generated by Django 4.1.7 on 2023-04-13 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0009_alter_features_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='features',
            name='change_audio_speed',
            field=models.BooleanField(default=False, verbose_name='تغيير سرعة الصوت'),
        ),
        migrations.AddField(
            model_name='features',
            name='change_img_size',
            field=models.BooleanField(default=False, verbose_name='تغيير حجم الصور'),
        ),
        migrations.AddField(
            model_name='features',
            name='change_video_speed',
            field=models.BooleanField(default=False, verbose_name='تغيير سرعة الفيديو'),
        ),
        migrations.AddField(
            model_name='features',
            name='remove_audio',
            field=models.BooleanField(default=False, verbose_name='إزالة الصوت من الفيديو'),
        ),
    ]