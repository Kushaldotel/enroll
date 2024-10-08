from django.core.management import call_command
from django.contrib import messages

def calculate_subjects_to_taught(modeladmin, request, queryset):
    try:
        call_command('subjectstaught')  # No arguments needed now
        messages.success(request, "Successfully calculated and stored subjects to be taught.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

def calculate_optimalsubjects(modeladmin, request, queryset):
    try:
        call_command('optimalsubjects')  # No arguments needed now
        messages.success(request, "Successfully calculated and stored subjects to be taught.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

def calculate_potentialsubjects(modeladmin, request, queryset):
    try:
        call_command('optitest3')  # No arguments needed now
        # call_command('optitest2')  # No arguments needed now
        messages.success(request, "Successfully calculated and stored subjects to be taught.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
