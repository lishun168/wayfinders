# Generated by Django 3.1.2 on 2021-07-21 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_auto_20210714_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 21, 13, 29, 2, 82706)),
        ),
        migrations.AddField(
            model_name='application',
            name='processsed',
            field=models.BooleanField(default=False),
        ),
    ]
