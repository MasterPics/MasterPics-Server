# Generated by Django 3.1.7 on 2021-05-15 07:12

import core.utils
import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone
import phone_field.models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.CharField(max_length=20, unique=True)),
                ('username', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('email_public', models.BooleanField(default=True)),
                ('category', models.CharField(choices=[('photographer', 'photographer'), ('model', 'model'), ('HairMakeup', 'HairMakeup'), ('stylist', 'stylist'), ('otheruse', 'otheruse')], max_length=20)),
                ('image', models.ImageField(blank=True, default='unnamed.png', upload_to=core.utils.uuid_name_upload_to)),
                ('desc', models.TextField(blank=True)),
                ('phone', phone_field.models.PhoneField(blank=True, max_length=31)),
                ('phone_public', models.BooleanField(default=True)),
                ('instagram', models.CharField(blank=True, max_length=20)),
                ('instagram_public', models.BooleanField(default=True)),
                ('is_ToS', models.BooleanField(default=False, validators=[user.models.is_ToS])),
                ('is_social', models.BooleanField(default=False)),
                ('user_identifier', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
