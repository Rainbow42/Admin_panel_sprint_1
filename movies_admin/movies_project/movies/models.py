from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FilmType(models.TextChoices):
    SERIES = 'series'
    FILM = 'movie'


class Profession(models.TextChoices):
    ACTORS = 'actor'
    DIRECTOR = 'director'
    WRITER = 'writer'


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
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
        blank=True,
        null=True,
        verbose_name='День рождения'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        index_together = ['first_name', 'last_name', 'patronymic']
        verbose_name = 'person'
        verbose_name_plural = 'persons'
        db_table = '"content"."person"'


class Genre(TimeStampedMixin, models.Model):
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

    def __str__(self):
        return str(self.name)

    class Meta:
        index_together = ['name']
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = 'content"."genre'


class FilmWork(TimeStampedMixin,models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
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
        validators=[MinValueValidator(1), MaxValueValidator(10)],
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
        default=uuid4
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
        auto_now_add=True
    )

    class Meta:
        index_together = ['film_work', 'genre']
        verbose_name = _('film genre')
        verbose_name_plural = _('film genres')
        db_table = '"content"."genre_film_work"'


class FilmWorkPersonsType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
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
        auto_now_add=True
    )

    class Meta:
        index_together = ['film_work', 'person']
        db_table = '"content"."person_film_work"'
