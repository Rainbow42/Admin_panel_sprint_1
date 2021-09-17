from django.contrib import admin

from users.models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'created_at',
    )
    list_filter = ('created_at',)
    search_fields = ('username', )


admin.site.register(Users, UsersAdmin)
