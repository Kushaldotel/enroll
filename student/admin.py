from django.contrib import admin
from .models import Student, CompletedSubject, UploadStudent
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

class StudentAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'dob', 'email', 'unique_username', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'unique_username', 'phone_number')
    list_filter = ('dob', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'middle_name', 'last_name', 'dob', 'email', 'unique_username', 'phone_number', 'completed_subjects', 'temporary_address', 'permanent_address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

class CompletedSubjectAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('student', 'subject', 'completion_date')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')


# class UploadStudentAdmin(ImportExportModelAdmin, ModelAdmin):
#     list_display = (
#         'first_name', 'middle_name', 'last_name', 'dob', 'email',
#         'unique_username', 'phone_number', 'created_at'
#     )
#     search_fields = (
#         'first_name', 'last_name', 'email', 'unique_username', 'phone_number'
#     )
#     list_filter = ('dob', 'created_at')
#     ordering = ('-created_at',)
#     readonly_fields = ('created_at', 'updated_at')
#     fieldsets = (
#         (None, {
#             'fields': (
#                 'first_name', 'middle_name', 'last_name', 'dob', 'email',
#                 'unique_username', 'phone_number', 'temporary_address',
#                 'permanent_address', 'completed_subjects'
#             )
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#         }),
#     )

# admin.site.register(UploadStudent, UploadStudentAdmin)

admin.site.register(CompletedSubject, CompletedSubjectAdmin)

admin.site.register(Student, StudentAdmin)