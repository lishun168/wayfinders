# Generated by Django 3.1.2 on 2021-08-05 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0027_auto_20210805_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 8, 5, 15, 12, 34, 543796)),
        ),
        migrations.AlterField(
            model_name='applicationupload',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 8, 5, 15, 12, 34, 544575)),
        ),
    ]