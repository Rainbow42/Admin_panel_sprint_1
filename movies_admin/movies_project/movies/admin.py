from django.contrib import admin


class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'rating', 'genre', 'age_censor', 'actors', 'file_path'
    )
    list_editable = ('genre', 'actors')
    # list_filter = ('flag', 'blogs',)
    # list_select_related = ('author',)
    # search_fields = ('title', 'author__username')
    # readonly_fields = ('updated_at', 'created_at')
    # raw_id_fields = ('author',)
    # filter_horizontal = ('blogs',)
    # actions = (
    #     'add_entries_to_search_index',
    #     'delete_entries_to_search_index',
    #     'delete_search_index'
    # )
