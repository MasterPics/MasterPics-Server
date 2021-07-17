
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.postbase')),
                ('file_attach', models.FileField(upload_to='')),
                ('pay', models.PositiveIntegerField()),
                ('pay_negotiation', models.BooleanField(default=False)),
                ('free', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_closed', models.BooleanField(default=False)),
                ('location', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='core.location')),
            ],
            bases=('core.postbase',),
        ),
    ]
