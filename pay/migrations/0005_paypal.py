# Generated by Django 4.1.7 on 2023-04-01 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0004_remove_subscription_end_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayPal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PAYPAL_CLIENT_ID', models.CharField(blank=True, max_length=255, null=True)),
                ('PAYPAL_SECRET', models.CharField(blank=True, max_length=255, null=True)),
                ('PAYPAL_ACCESS_TOKEN', models.TextField(blank=True, null=True)),
                ('PAYPAL_CURRENCY', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'Paypal',
                'verbose_name_plural': 'Paypals',
            },
        ),
    ]
