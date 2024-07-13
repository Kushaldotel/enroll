# In subject/admin.py

from django.contrib import admin
from .models import Subject
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

class SubjectAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('name', 'code', 'department', 'credits')
    list_filter = ('department',)
    search_fields = ('name', 'code', 'department')
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'description', 'credits', 'department')
        }),
        ('Important dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Subject, SubjectAdmin)
