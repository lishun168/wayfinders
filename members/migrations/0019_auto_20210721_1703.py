# Generated by Django 3.1.2 on 2021-07-21 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0018_auto_20210721_1702'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='processsed',
            new_name='approved',
        ),
        migrations.RenameField(
            model_name='applicationupload',
            old_name='processsed',
            new_name='approved',
        ),
        migrations.AddField(
            model_name='application',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicationupload',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='application',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 21, 17, 3, 24, 626650)),
        ),
        migrations.AlterField(
            model_name='applicationupload',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 21, 17, 3, 24, 627305)),
        ),
    ]