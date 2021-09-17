from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseFilm(models.Model):
    id = models.UUIDField(
        verbose_name='UUID',
        default=uuid4,
        unique=True,
        primary_key=True
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        db_index=True
    )
    description = models.TextField(
        _('description'),
        blank=True
    )
    rating = models.FloatField(
        _('rating'),
        validators=[MinValueValidator(0)],
        blank=True
    )
    created_at = models.DateField(
        default=timezone.now,
        db_index=True,
        verbose_name=_('created_at'),
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        abstract = True
