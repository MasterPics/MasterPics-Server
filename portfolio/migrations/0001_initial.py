<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-07-15 15:14
=======
<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-05-28 09:46

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
=======
<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-07-15 15:00
=======
# Generated by Django 3.1.7 on 2021-07-15 06:46
>>>>>>> comment
>>>>>>> develop

from django.db import migrations, models
import django.db.models.deletion
>>>>>>> develop


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
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedPortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_taggedportfolio_items', to='taggit.tag')),
                ('tags', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tagged_portfolios', to='portfolio.tag')),
=======
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.postbase')),
>>>>>>> develop
            ],
            bases=('core.postbase',),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='thumbnail',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_thumbnail', to='core.images'),
        ),
    ]
