# Generated by Django 5.0.1 on 2024-01-20 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_room_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.IntegerField(),
        ),
    ]
