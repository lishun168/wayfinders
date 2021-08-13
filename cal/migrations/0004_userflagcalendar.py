# Generated by Django 3.1.2 on 2021-08-04 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0022_auto_20210804_1945'),
        ('cal', '0003_calendar_number_of_flags'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFlagCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flagged', models.BooleanField(default=False)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cal.calendar')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.memberuser')),
            ],
        ),
    ]
