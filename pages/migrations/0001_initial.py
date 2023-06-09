# Generated by Django 4.1.7 on 2023-04-14 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='البريد الإلكتروني')),
                ('plan', models.CharField(max_length=100, verbose_name='الباقة')),
                ('details', models.TextField(verbose_name='التفاصيل')),
            ],
            options={
                'verbose_name': 'طلب',
                'verbose_name_plural': 'طلبات التواصل',
            },
        ),
    ]
