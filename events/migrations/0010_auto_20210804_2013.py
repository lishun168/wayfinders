# Generated by Django 3.1.2 on 2021-08-04 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20210804_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('A', 'Appointment'), ('M', 'Meeting')], max_length=1),
        ),
    ]