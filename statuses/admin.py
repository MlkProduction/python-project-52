from django.contrib import admin
from statuses.models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
