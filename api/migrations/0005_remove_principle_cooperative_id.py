# Generated by Django 2.2.2 on 2019-12-28 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20191228_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='principle',
            name='cooperative_id',
        ),
    ]
