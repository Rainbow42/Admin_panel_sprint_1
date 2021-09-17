from django.db import models
from django.utils.translation import gettext_lazy as _

from movies.models import Genre, TimeStampedMixin
from persons.models import Person
from utils.base_model import BaseFilm


class Serieswork(BaseFilm, TimeStampedMixin):
    genre = models.ManyToManyField(Genre)
    person = models.ManyToManyField(Person)
    file_path = models.FileField(_('file'), upload_to='series_works/', blank=True)

    class Meta:
        verbose_name = 'series'
        verbose_name_plural = 'series'
        db_table = "content.series_work"
