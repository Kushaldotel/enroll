# In teacher/admin.py

from django.contrib import admin
from .models import Teacher
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
class TeacherAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('email', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'department')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_name', 'last_name', 'dob', 'email', 'unique_username', 'phone_number')
        }),
        ('Professional Information', {
            'fields': ('department',),
        }),
        ('Important dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Teacher, TeacherAdmin)
