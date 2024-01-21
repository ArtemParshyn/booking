# Generated by Django 5.0.1 on 2024-01-21 21:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_booking_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel', to='api.hotel'),
        ),
    ]