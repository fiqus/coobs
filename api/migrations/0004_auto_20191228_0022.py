# Generated by Django 2.2.2 on 2019-12-28 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_load_principles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='cooperative',
            new_name='cooperative_id',
        ),
        migrations.RenameField(
            model_name='partner',
            old_name='cooperative',
            new_name='cooperative_id',
        ),
        migrations.RenameField(
            model_name='period',
            old_name='cooperative',
            new_name='cooperative_id',
        ),
        migrations.RenameField(
            model_name='principle',
            old_name='cooperative',
            new_name='cooperative_id',
        ),
    ]
