# Generated by Django 3.1.2 on 2021-09-01 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0005_filter_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='color',
            field=models.CharField(default='#eb3434', max_length=255),
        ),
    ]
