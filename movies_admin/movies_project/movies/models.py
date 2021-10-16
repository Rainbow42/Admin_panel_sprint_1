import uuid
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from persons.models import Person


class TimeStampedMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Genre(models.Model):
    id = models.UUIDField(
        default=uuid4,
        unique=True,
        verbose_name='UUID',
        primary_key=True
    )
    title = models.CharField(_('title'), max_length=255)

    def __str__(self):
        return str(self.title)

    class Meta:
        index_together = ['title']
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = 'content"."genre'


class Filmwork(models.Model):
    class FilmType(models.TextChoices):
        SERIES = 'series'
        FILM = 'film'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(
        _('title'),
        max_length=255,
        db_index=True
    )
    description = models.TextField(
        _('description'),
        blank=True,
        null=True
    )
    imdb_rating = models.FloatField(
        _('imdb_rating'),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    ratings = models.IntegerField(
        _('rating'),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True, null=True)
    genre = models.ManyToManyField(Genre, through="FilmworkGenres", related_name="genre", blank=True)
    person = models.ManyToManyField(Person, through="FilmworkPersonsType", related_name="person", blank=True)
    age_censor = models.IntegerField(_('censor'), blank=True, null=True)
    type = models.CharField(
        max_length=6,
        default=FilmType.FILM,
        choices=FilmType.choices,
        verbose_name='Тип',
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.title} {self.type}"

    class Meta:
        index_together = ['title']
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = '"content"."film_work"'


class FilmworkGenres(models.Model):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('film genre')
        verbose_name_plural = _('film genres')
        db_table = '"content"."film_work_genre"'


class FilmworkPersonsType(models.Model):
    class Profession(models.TextChoices):
        ACTORS = 'actors'
        DIRECTOR = 'directions'
        WRITER = 'writers'

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    type_person = models.CharField(
        max_length=11,
        blank=True,
        choices=Profession.choices,
        verbose_name='Профессия',
    )

    class Meta:
        db_table = '"content"."film_work_persons_type"'
