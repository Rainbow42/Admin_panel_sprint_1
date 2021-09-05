from django.db import models
from django.utils.translation import gettext_lazy as _

from persons.models import Person
from utils.base_model import BaseFilm


class TimeStampedMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Genre(TimeStampedMixin, models.Model):
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = "content.genre"


class Filmwork(BaseFilm, TimeStampedMixin):
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True)
    genre = models.ManyToManyField(Genre)
    person = models.ManyToManyField(Person)
    age_censor = models.IntegerField(_('censor'))

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = "content.film_work"
