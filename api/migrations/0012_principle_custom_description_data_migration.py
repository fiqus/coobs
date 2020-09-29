from django.db import migrations

def set_default_description(apps, schema_editor):
    Principle = apps.get_model("api", "Principle")
    for principle in Principle.objects.all():
        principle.custom_description = "" if not principle.custom_description else principle.custom_description
        principle.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_principle_custom_description'),
    ]

    operations = [
        migrations.RunPython(set_default_description),
    ]
