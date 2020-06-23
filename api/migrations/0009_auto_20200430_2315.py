# Generated by Django 2.2.10 on 2020-04-30 23:15

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200424_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='SDGObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_to_reach', models.DecimalField(blank=True, decimal_places=1, default=Decimal('0.0'), max_digits=19, null=True, verbose_name='hours to invest')),
                ('money_to_invest', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=19, null=True, verbose_name='money to invest')),
                ('actions_to_perform', models.PositiveIntegerField(blank=True, null=True, verbose_name='actions quantity to perform')),
                ('cooperative', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Cooperative', verbose_name='cooperative')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Period', verbose_name='period')),
                ('sustainable_development_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SustainableDevelopmentGoal', verbose_name='sustainable_development_goal')),
            ],
            options={
                'verbose_name': 'sdgObjective',
            },
        ),
        migrations.AddConstraint(
            model_name='sdgobjective',
            constraint=models.UniqueConstraint(fields=('cooperative', 'period', 'sustainable_development_goal'), name='unique_objective'),
        ),
    ]
