# Generated by Django 3.1.2 on 2021-08-04 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0002_auto_20210519_0520'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='number_of_flags',
            field=models.IntegerField(default=0),
        ),
    ]
