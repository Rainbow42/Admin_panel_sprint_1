from django.contrib import admin
from persons.models import Person


@admin.register(Person)
class Person(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'patronymic', 'birthdate'
    )
    readonly_fields = ('id',)
    search_fields = ('first_name', 'last_name', 'patronymic')
    fields = (
        'id', 'first_name', 'last_name', 'patronymic', 'birthdate'
    )

