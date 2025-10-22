from django.contrib import admin

# Register your models here.
from .models import StoredString

@admin.register(StoredString)
class StoredStringAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'created_at')
    search_fields = ('value', 'id')
