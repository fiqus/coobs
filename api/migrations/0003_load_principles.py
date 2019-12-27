import os
from django.core.management import call_command
from django.db import migrations

fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))


def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, 'cooperatives.json')
    call_command('loaddata', fixture_file, app_label='api')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_load_cooperatives'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
