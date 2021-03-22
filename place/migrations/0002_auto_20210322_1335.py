# Generated by Django 3.1.7 on 2021-03-22 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20210322_1335'),
        ('place', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='like_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='place',
            name='location',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='core.location'),
        ),
        migrations.AddField(
            model_name='place',
            name='save_users',
            field=models.ManyToManyField(blank=True, related_name='save_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='place',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='places', to='core.Tag'),
        ),
        migrations.AddField(
            model_name='place',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
