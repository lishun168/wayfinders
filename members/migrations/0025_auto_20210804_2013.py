# Generated by Django 3.1.2 on 2021-08-04 20:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0024_auto_20210804_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 8, 4, 20, 13, 55, 687783)),
        ),
        migrations.AlterField(
            model_name='applicationupload',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 8, 4, 20, 13, 55, 688487)),
        ),
    ]
