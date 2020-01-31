import os
from django.core.management import call_command
from django.db import migrations, models

fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))


def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, 'principles.json')
    call_command('loaddata', fixture_file, app_label='api')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainprinciple',
            name='description_en',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='mainprinciple',
            name='description_es',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.RunPython(load_fixture),
    ]
