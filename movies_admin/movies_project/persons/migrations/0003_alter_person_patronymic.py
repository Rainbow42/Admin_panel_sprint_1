# Generated by Django 3.2.7 on 2021-10-16 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_person_film'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='patronymic',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Отчество'),
        ),
    ]