# Generated by Django 3.2.7 on 2021-10-16 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0007_auto_20211016_1252'),
        ('movies', '0011_auto_20211016_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmworkpersonstype',
            name='person',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='persons.person'),
        ),
    ]
