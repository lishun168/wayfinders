# Generated by Django 3.1.2 on 2021-08-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_userflagevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('M', 'Meeting'), ('A', 'Appointment')], max_length=1),
        ),
    ]
