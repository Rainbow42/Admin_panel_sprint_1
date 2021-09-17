from django.contrib import admin

from series.models import Serieswork


class SeriesworkAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'rating', 'file_path'
    )
    list_filter = ('rating', 'created_at')
    search_fields = ('title', )


admin.site.register(Serieswork, SeriesworkAdmin)
