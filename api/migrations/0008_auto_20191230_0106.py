# Generated by Django 2.2.2 on 2019-12-30 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20191228_1433'),
    ]

    operations = [
        migrations.RenameField(
            model_name='period',
            old_name='cooperative_id',
            new_name='cooperative',
        ),
    ]