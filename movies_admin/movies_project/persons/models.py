from uuid import uuid4

from django.db import models


class Person(models.Model):
    class Profession(models.IntegerChoices):
        ACTORS = 1, 'Актер'
        DIRECTOR = 2, 'Режиссер'
        WRITER = 3, 'Сценарист'

    uuid = models.UUIDField(verbose_name='UUID', default=uuid4, unique=True)
    first_name = models.CharField('Имя', max_length=250, blank=True)
    last_name = models.CharField('Фамилия', max_length=250, blank=True)
    profession_type = models.CharField('Профессия', max_length=10, choices=Profession.choices)

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'persons'
        db_table = "content.person"
