<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-07-15 15:00
=======
# Generated by Django 3.1.7 on 2021-07-15 06:46
>>>>>>> comment

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('place', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='places', to=settings.AUTH_USER_MODEL),
        ),
    ]
