from django.contrib import admin

from movies.models import Filmwork, Genre


class FikmworkAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'rating', 'age_censor', 'file_path'
    )
    list_filter = ('rating', 'age_censor', 'created_at')
    search_fields = ('title', )


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description'
    )
    search_fields = ('name', )


admin.site.register(Filmwork, FikmworkAdmin)
admin.site.register(Genre, GenreAdmin)
