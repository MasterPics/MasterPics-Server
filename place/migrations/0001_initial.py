<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-07-16 10:26
=======
# Generated by Django 3.1.7 on 2021-07-16 09:52
>>>>>>> contact

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
<<<<<<< HEAD
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.postbase')),
=======
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desc', models.TextField()),
>>>>>>> contact
                ('pay', models.PositiveIntegerField()),
                ('free', models.BooleanField(default=False)),
                ('location', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='core.location')),
                ('thumbnail', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='place_thumbnail', to='core.images')),
            ],
            bases=('core.postbase',),
        ),
    ]
