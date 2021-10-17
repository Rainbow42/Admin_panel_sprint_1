import uuid
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from persons.models import Person


class Genre(models.Model):
    id = models.UUIDField(
        default=uuid4,
        unique=True,
        verbose_name='UUID',
        primary_key=True
    )
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        index_together = ['name']
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = 'content"."genre'


class FilmWork(models.Model):
    class FilmType(models.TextChoices):
        SERIES = 'series'
        FILM = 'movie'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="Наименование"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        verbose_name="Рейтинг"
    )
    certificate = models.CharField(
        blank=True,
        null=True,
        max_length=4,
        verbose_name="Возрастной рейтинг"
    )
    creation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата выхода фильма"
    )
    file_path = models.FileField(
        upload_to='film_works/',
        blank=True,
        null=True,
        verbose_name="Директория"
    )
    genre = models.ManyToManyField(
        Genre,
        through="FilmWorkGenres",
        related_name="genre",
        blank=True
    )
    person = models.ManyToManyField(
        Person,
        through="FilmWorkPersonsType",
        related_name="person",
        blank=True,
        verbose_name="Персона"
    )
    type = models.CharField(
        max_length=6,
        default=FilmType.FILM,
        choices=FilmType.choices,
        verbose_name='Тип',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} {self.type}"

    class Meta:
        index_together = ['title']
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = '"content"."film_work"'


class FilmWorkGenres(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    class Meta:
        verbose_name = _('film genre')
        verbose_name_plural = _('film genres')
        db_table = '"content"."genre_film_work"'


class FilmWorkPersonsType(models.Model):
    class Profession(models.TextChoices):
        ACTORS = 'actor'
        DIRECTOR = 'director'
        WRITER = 'writer'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        blank=True
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        blank=True
    )
    role = models.CharField(
        max_length=11,
        blank=True,
        choices=Profession.choices,
        verbose_name='Профессия',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    class Meta:
        db_table = '"content"."person_film_work"'
