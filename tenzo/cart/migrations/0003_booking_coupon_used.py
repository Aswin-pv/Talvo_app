# Generated by Django 4.2.7 on 2024-07-03 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='coupon_used',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
