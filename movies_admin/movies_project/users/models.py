import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.core import validators
from django.db import models
from django.utils import timezone


class Users(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        help_text='Обязательное. Не более 150 символов.',
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                (
                    'Введите имя пользователя. '
                    'Может содержать только буквы, цифры и '
                    'символы @/./+/-/_'
                ), 'invalid'
            ),
        ],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует',
        },
        db_index=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=250,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=250,
        blank=True
    )
    email = models.EmailField(
        'Email',
        max_length=250
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        blank=True,
        default=timezone.now
    )
    permissions = ArrayField(
        models.CharField(max_length=255, blank=True),
        size=8,
        blank=True,
        default=list
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username}"

    def __unicode__(self):
        if self.last_name and self.first_name and self.username:
            return f'{self.last_name} {self.first_name} ({self.username})'
        return str(self.username)

    class Meta:
        index_together = ['first_name', 'last_name', 'username']
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = '"content"."users"'
