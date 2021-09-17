from uuid import uuid4

from django.db import models


class Person(models.Model):
    class Profession(models.IntegerChoices):
        ACTORS = 1, 'Актер'
        DIRECTOR = 2, 'Режиссер'
        WRITER = 3, 'Сценарист'

    uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        verbose_name='UUID'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=250
    )
    last_name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Фамилия'
    )
    profession_type = models.CharField(
        max_length=10,
        blank=True,
        choices=Profession.choices,
        verbose_name='Профессия',
    )

    def __str__(self):
        return f"{self.first_name}"

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'persons'
        db_table = "content.person"
