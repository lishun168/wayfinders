# Generated by Django 3.1.2 on 2021-05-18 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20210518_1905'),
        ('industries', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MemberToIndustory',
            new_name='MemberToIndustry',
        ),
    ]
