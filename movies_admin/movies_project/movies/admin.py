from django.contrib import admin

from movies.models import Filmwork, Genre


class PersonInstanceInline(admin.TabularInline):
    model = Filmwork.person.through


class GenreInstanceInline(admin.TabularInline):
    model = Filmwork.genre.through


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'id', 'title',
    )
    search_fields = ('title',)


@admin.register(Filmwork)
class FikmworkAdmin(admin.ModelAdmin):
    inlines = [PersonInstanceInline, GenreInstanceInline]
    readonly_fields = ('id',)
    list_display = (
        'id', 'title', 'description', 'ratings', 'age_censor', 'file_path', 'type'
    )
    list_filter = ('ratings', 'age_censor', 'type')
    search_fields = ('title',)

    def get_queryset(self, request):
        return super(FikmworkAdmin, self).get_queryset(request).prefetch_related('person', 'genre')
