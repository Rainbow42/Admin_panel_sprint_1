from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseFilm(models.Model):
    id = models.UUIDField(verbose_name='UUID', default=uuid4, unique=True, primary_key=True)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0)], blank=True)

    class Meta:
        abstract = True
