# Generated by Django 3.1.7 on 2021-06-28 14:53

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('core', '0001_initial'),
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
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PortfolioInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='portfolioInformation_set', to='core.information')),
                ('portfolio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.images')),
                ('portfolio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_images', to='portfolio.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.comment')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio')),
            ],
        ),
        migrations.AddField(
            model_name='portfolio',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='portfolio.TaggedPortfolio', to='taggit.Tag', verbose_name='tags'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='thumbnail',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_thumbnail', to='core.images'),
        ),
    ]
