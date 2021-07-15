<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-07-14 06:15
=======
# Generated by Django 3.1.7 on 2021-07-15 05:12
>>>>>>> postBase

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.postbase')),
            ],
            bases=('core.postbase',),
        ),
    ]
