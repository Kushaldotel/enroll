from django.core.management.base import BaseCommand
from student.models import Student
from subject.models import Subject
from student.models import CompletedSubject

class Command(BaseCommand):
    help = 'Print student ID and subject IDs of remaining subjects for each student, ordered by student ID'

    def handle(self, *args, **kwargs):
        # Get all students, ordered by ID
        all_students = Student.objects.all().order_by('id')
        all_subjects = Subject.objects.all()

        # Iterate through each student and calculate remaining subjects
        for student in all_students:
            student_id = student.id

            # Get subjects the student has already completed
            completed_subjects = CompletedSubject.objects.filter(student=student).values_list('subject', flat=True)

            # Calculate remaining subjects
            remaining_subjects = list(all_subjects.exclude(id__in=completed_subjects).values_list('id', flat=True))

            # Print the student ID and their remaining subjects' IDs
            self.stdout.write(f"Student ID: {student_id}")
            self.stdout.write(f"Remaining Subject IDs: {', '.join(map(str, remaining_subjects)) if remaining_subjects else 'None'}\n")

        self.stdout.write(self.style.SUCCESS('Finished printing remaining subjects (with IDs) for each student, ordered by student ID.'))
