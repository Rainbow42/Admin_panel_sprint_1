from django.contrib import admin
from movies.models import FilmWork, Genre


class PersonInstanceInline(admin.TabularInline):
    model = FilmWork.person.through


class GenreInstanceInline(admin.TabularInline):
    model = FilmWork.genre.through


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'id', 'name', 'description', 'created_at', 'updated_at'
    )
    search_fields = ('name',)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = [PersonInstanceInline, GenreInstanceInline]
    readonly_fields = ('id',)
    list_display = (
        'id', 'title', 'description', 'rating', 'certificate', 'file_path', 'type'
    )
    fields = (
        'id', 'title', 'description', 'rating', 'certificate', 'file_path',
        'type', 'created_at', 'updated_at'
    )
    list_filter = ('rating', 'certificate', 'type')
    search_fields = ('title',)

    def get_queryset(self, request):
        return super(FilmWorkAdmin, self).get_queryset(request).prefetch_related('person', 'genre')
