
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
                ('file_attach', models.FileField(null=True, upload_to='')),
                ('pay', models.PositiveIntegerField(blank=True, default=0)),
                ('pay_type', models.IntegerField(choices=[(0, '상호 무페이'), (1, '페이 입력'), (2, '페이 협의')], default=0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_closed', models.BooleanField(default=False)),
                ('location', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='core.location')),
            ],
            bases=('core.postbase',),
        ),
    ]
