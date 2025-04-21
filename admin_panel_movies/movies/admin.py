from django.contrib import admin

from .models import FilmWork, Genre, Person, PersonFilmWork, GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1  # Количество пустых строк для добавления новых персон
    autocomplete_fields = ["person"]  # Удобный поиск по персоне
    verbose_name = "Персона в фильме"
    verbose_name_plural = "Персоны в фильме"


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 1
    autocomplete_fields = ["genre"]
    verbose_name = "Жанр фильма"
    verbose_name_plural = "Жанры фильма"


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "rating", "modified_at")
    search_fields = ("title",)
    list_filter = ("type", "creation_date")
    inlines = [
        PersonFilmWorkInline,
        GenreFilmWorkInline,
    ]  # Добавляем связь персон в админке фильма


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)
