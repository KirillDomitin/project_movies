from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .genre import Genre
from .mixins import TimeStampedMixin, UUIDMixin
from .person import Person


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        MOVIE = "movie", _("Фильм")
        SERIES = "series", _("Сериал")
        TV_SHOW = "tv show", _("Передача")

    title = models.TextField(verbose_name=_("Название фильма"))
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Описание фильма")
    )
    creation_date = models.DateField(
        blank=True, null=True, verbose_name=_("Дата выхода фильма")
    )
    persons = models.ManyToManyField(Person, through="PersonFilmwork")
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    rating = models.FloatField(
        verbose_name=_("Рейтинг"),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],  # Ограничение рейтинга от 0 до 10
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=10, choices=FilmType.choices, verbose_name=_("Тип фильма")
    )
    certificate = models.CharField(_("Сертификат"), max_length=512, blank=True)
    file_path = models.FileField(_("Файл"), blank=True, null=True, upload_to="movies/")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Фильм")
        verbose_name_plural = _("Фильмы")

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, related_name="genre_film_works"
    )
    film_work = models.ForeignKey(
        "FilmWork", on_delete=models.CASCADE, related_name="film_genres"
    )

    class Meta:
        db_table = 'content"."genre_film_work'


class PersonFilmWork(UUIDMixin):
    class RoleType(models.TextChoices):
        ACTOR = "actor", _("Актер")
        DIRECTOR = "director", _("Режиссер")
        WRITER = "writer", _("Сценарист")

    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="person_film_works"
    )
    film_work = models.ForeignKey(
        "FilmWork", on_delete=models.CASCADE, related_name="film_persons"
    )
    role = models.CharField(
        max_length=20, choices=RoleType.choices, verbose_name=_("Роль")
    )

    class Meta:
        db_table = 'content"."person_film_work'
