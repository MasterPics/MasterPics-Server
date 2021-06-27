# Generated by Django 3.1.7 on 2021-06-27 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desc', models.TextField()),
                ('pay', models.PositiveIntegerField()),
                ('free', models.BooleanField(default=False)),
                ('location', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='core.location')),
                ('thumbnail', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_thumbnail', to='core.images')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.information')),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='place.place')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.images')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_images', to='place.place')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.comment')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='place.place')),
            ],
        ),
    ]
