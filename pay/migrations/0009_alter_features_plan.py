# Generated by Django 4.1.7 on 2023-04-13 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0008_remove_features_videotemplates_features_template1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='features',
            name='plan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pay.plan'),
        ),
    ]
