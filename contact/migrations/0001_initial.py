# Generated by Django 3.1.7 on 2021-06-13 08:48

import contact.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(upload_to=contact.utils.uuid_name_upload_to, verbose_name='Image')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desc', models.TextField()),
                ('file_attach', models.FileField(upload_to='')),
                ('pay', models.PositiveIntegerField()),
                ('pay_negotiation', models.BooleanField(default=False)),
                ('free', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_closed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ContactInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contact.contact')),
            ],
        ),
    ]
