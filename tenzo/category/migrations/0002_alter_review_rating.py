# Generated by Django 4.2.7 on 2024-01-22 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], max_length=150),
        ),
    ]
