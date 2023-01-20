# Generated by Django 3.2.16 on 2023-01-17 07:13

import base.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, unique=True, verbose_name='name')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='permissions')),
            ],
            managers=[
                ('objects', base.models.UserTypeManager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(error_messages={'invalid': 'Enter a valid email address.', 'null': 'Email field is required.', 'unique': 'An account with that email already exists. Please login to continue.'}, max_length=127, unique=True, verbose_name='Email')),
                ('username', models.CharField(error_messages={'invalid': 'Enter a valid username.', 'null': 'Username field is required.', 'unique': 'An account with that username already exists.'}, help_text='Better to use your email address all characters before @.', max_length=127, unique=True, verbose_name='Username')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Full Name')),
                ('contact_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Contact Number')),
                ('avatar', models.ImageField(blank=True, default=base.models.get_default_avatar, null=True, upload_to=base.models.get_user_avatar, verbose_name='Avatar')),
                ('is_email_verified', models.BooleanField(default=base.models.get_email_verified_value, help_text='Designates whether this user is verified or not.', verbose_name='Email Verification Status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Staff Status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.Unselect this field instead of deleting accounts.', verbose_name='Active')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last Login')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', null=True, related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='Groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', null=True, related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('user_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_type', to='base.usertype')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['-date_joined'],
            },
        ),
    ]