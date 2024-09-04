# Generated by Django 5.1 on 2024-09-04 14:24

import django.db.models.deletion
import schemes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemes', '0008_alter_schemecriteria_criteria_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemecriteria',
            name='criteria_operator',
            field=models.CharField(choices=[('LESS_THAN', 'LESS_THAN'), ('LESS_THAN_EQUAL', 'LESS_THAN_EQUAL'), ('EQUAL', 'EQUAL'), ('GREATER_THAN_EQUAL', 'GREATER_THAN_EQUAL'), ('GREATER_THAN', 'GREATER_THAN'), ('LENGTH_LESS_THAN', 'LENGTH_LESS_THAN'), ('LENGTH_LESS_THAN_EQUAL', 'LENGTH_LESS_THAN_EQUAL'), ('LENGTH_EQUAL', 'LENGTH_EQUAL'), ('LENGTH_GREATER_THAN', 'LENGTH_GREATER_THAN'), ('LENGTH_GREATER_THAN_EQUAL', 'LENGTH_GREATER_THAN_EQUAL'), ('STRING_EQUAL', 'STRING_EQUAL')], default=schemes.models.SCHEME_CRITERIA_OPERATOR['EQUAL'], max_length=28),
        ),
        migrations.AlterField(
            model_name='schemecriteria',
            name='criteria_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='criterias', to='schemes.criteriaset'),
        ),
    ]
