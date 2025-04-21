from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import UUIDMixin, TimeStampedMixin


class Gender(models.TextChoices):
    MALE = "male", _("Мужской")
    FEMALE = "female", _("Женский")


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("Полное имя"), max_length=255)
    gender = models.TextField(_("Пол"), choices=Gender.choices, null=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = 'content"."person'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _("Персона")
        verbose_name_plural = _("Персоны")

    def __str__(self):
        return self.full_name
