import uuid

from django.db import models


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=250
    )
    last_name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Фамилия'
    )
    patronymic = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name='Отчество'
    )
    birthdate = models.DateField(
        verbose_name='День рождения'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        index_together = ['first_name', 'last_name', 'patronymic']
        verbose_name = 'person'
        verbose_name_plural = 'persons'
        db_table = '"content"."person"'



