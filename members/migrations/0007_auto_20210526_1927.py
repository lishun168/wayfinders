# Generated by Django 3.1.2 on 2021-05-26 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_member_business_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('org_name', models.CharField(max_length=255)),
                ('org_email', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
        ),
        migrations.AlterField(
            model_name='member',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]