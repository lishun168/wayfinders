# Generated by Django 3.1.2 on 2021-08-04 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='number_of_flags',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('A', 'Appointment'), ('M', 'Meeting')], max_length=1),
        ),
    ]
