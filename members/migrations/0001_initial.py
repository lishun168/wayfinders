# Generated by Django 3.1.2 on 2021-05-18 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('main_image', models.ImageField(blank=True, upload_to='profile_gallery')),
                ('public', models.BooleanField(default=True)),
                ('logo', models.ImageField(blank=True, upload_to='group_logo')),
                ('website', models.URLField(blank=True, max_length=255, null=True)),
                ('business_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('address_2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=255, null=True)),
                ('membership_expiry', models.DateField(blank=True, null=True)),
                ('membership_since', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('can_create_forum_group', models.BooleanField(default=False)),
                ('can_post_to_forums', models.BooleanField(default=False)),
                ('can_add_calendar_events', models.BooleanField(default=False)),
                ('can_see_all_members', models.BooleanField(default=False)),
                ('can_edit_company_profile', models.BooleanField(default=False)),
                ('can_see_company_console', models.BooleanField(default=False)),
                ('can_add_employees', models.BooleanField(default=False)),
                ('can_delete_posts', models.BooleanField(default=False)),
                ('is_account_manager', models.BooleanField(default=False)),
                ('is_calendar_manager', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_permissions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.userrole')),
            ],
            options={
                'verbose_name': 'Permission',
                'verbose_name_plural': 'Permissions',
            },
        ),
        migrations.CreateModel(
            name='MemberUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('job_title', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('address_2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=255, null=True)),
                ('business_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('home_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('cell_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('bio', models.TextField(blank=True, null=True)),
                ('publicly_viewable', models.BooleanField(default=True, verbose_name='Public')),
                ('membership_since', models.DateField(blank=True, null=True)),
                ('main_image', models.ImageField(blank=True, upload_to='profile_gallery')),
                ('is_forum_mod', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
                ('search_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.searchobject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Member User',
                'verbose_name_plural': 'Member Users',
            },
        ),
        migrations.CreateModel(
            name='MemberCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_since', models.DateField(blank=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='members.userrole')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.memberuser')),
            ],
            options={
                'verbose_name': 'Member Companies',
                'verbose_name_plural': 'Member Companies',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='members/static/members/gallery/')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Galleries',
            },
        ),
    ]