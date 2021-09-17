from django.contrib import admin

from persons.models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'first_name', 'last_name', 'profession_type',
    )
    list_filter = ('profession_type', )
    search_fields = ('title', )


admin.site.register(Person, PersonAdmin)
