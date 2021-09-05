# Generated by Django 3.2 on 2021-09-05 19:17

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует'}, help_text='Обязательное. Не более 150 символов.', max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Введите имя пользователя. Может содержать только буквы, цифры и символы @/./+/-/_', 'invalid')], verbose_name='Имя пользователя')),
                ('first_name', models.CharField(blank=True, db_index=True, max_length=250, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=250, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=250, verbose_name='Email')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'content.users',
            },
        ),
    ]
