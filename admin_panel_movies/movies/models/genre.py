from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import UUIDMixin, TimeStampedMixin


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('Название'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('Описание'), blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')

    def __str__(self):
        return self.name
