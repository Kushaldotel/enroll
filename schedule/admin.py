# In schedule/admin.py

from django.contrib import admin
from .models import Schedule
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from subject.models import PotentialSubject, SubjectToTaught, AllocatedSubject, NewPotentialSubject
from .admin_actions import calculate_subjects_to_taught, calculate_optimalsubjects
from django.shortcuts import redirect

class ScheduleAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('teacher', 'subject', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'teacher', 'subject')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'subject__name')
    fieldsets = (
        (None, {
            'fields': ('teacher', 'subject', 'day_of_week', 'start_time', 'end_time')
        }),
        ('Important dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

# class PotentialSubjectAdmin(ModelAdmin,ImportExportModelAdmin):
#     list_display = ('subject', 'remaining_students')
#     search_fields = ('subject__name',)


class SubjectToTaughtAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('number_of_subjects', 'subject_names_display')
    search_fields = ('subject_names',)

    # actions = [calculate_subjects_to_taught]
    actions = [calculate_optimalsubjects]

    def subject_names_display(self, obj):
        return ', '.join(obj.subject_names)
    subject_names_display.short_description = 'Subjects'

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] == 'calculate_optimalsubjects':
            return self.calculate_optimalsubjects(request)
        return super().changelist_view(request, extra_context=extra_context)

    def calculate_optimalsubjects(self, request):
        calculate_optimalsubjects(self, request, None)
        return redirect('..')  # Redirect back to the changelist view

    # def calculate_subjects(self, request):
    #     calculate_subjects_to_taught(self, request, None)
    #     return redirect('..')  # Redirect back to the changelist view

class AllocatedSubjectAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('student', 'allocated_subjects_display')
    search_fields = ('student__first_name', 'student__last_name', 'allocated_subjects')

    def allocated_subjects_display(self, obj):
        return ', '.join(obj.allocated_subjects)
    allocated_subjects_display.short_description = 'Allocated Subjects'


class NewPotentialSubjectAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('subject', 'remaining_students')
    search_fields = ('subject__name',)

admin.site.register(NewPotentialSubject, NewPotentialSubjectAdmin)

admin.site.register(AllocatedSubject, AllocatedSubjectAdmin)

admin.site.register(SubjectToTaught, SubjectToTaughtAdmin)

# admin.site.register(PotentialSubject, PotentialSubjectAdmin)

admin.site.register(Schedule, ScheduleAdmin)
