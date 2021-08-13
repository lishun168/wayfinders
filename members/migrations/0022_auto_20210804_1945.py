# Generated by Django 3.1.2 on 2021-08-04 19:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0021_auto_20210804_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 8, 4, 19, 45, 2, 474418)),
        ),
        migrations.AlterField(
            model_name='applicationupload',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 8, 4, 19, 45, 2, 475065)),
        ),
        migrations.CreateModel(
            name='UserFlagUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flagged', models.BooleanField(default=False)),
                ('flagged_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flagged_user', to='members.memberuser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.memberuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserFlagMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flagged', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.memberuser')),
            ],
        ),
    ]
