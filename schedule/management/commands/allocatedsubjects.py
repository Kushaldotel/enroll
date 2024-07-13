from django.core.management.base import BaseCommand
from student.models import Student
from subject.models import Subject, PotentialSubject, AllocatedSubject
from student.models import CompletedSubject

class Command(BaseCommand):
    help = 'Allocate subjects to students based on potential subjects and the number of subjects to be taught by college'

    def handle(self, *args, **kwargs):
        # Define the number of subjects to be taught by the college
        subjects_to_taught = 2  # or 3, or any other number as per your requirement

        # Clear existing AllocatedSubject data
        AllocatedSubject.objects.all().delete()

        # Get all students
        all_students = Student.objects.all()

        # Get the potential subjects sorted by the number of remaining students
        potential_subjects = PotentialSubject.objects.all().order_by('-remaining_students')

        # Create a dictionary to store the allocated subjects for each student
        student_allocations = {student: [] for student in all_students}

        # Allocate subjects based on the subjects_to_taught flag
        for potential_subject in potential_subjects:
            if len(student_allocations[potential_subject.subject]) >= subjects_to_taught:
                continue

            for student in all_students:
                completed_subjects = CompletedSubject.objects.filter(student=student).values_list('subject', flat=True)
                if potential_subject.subject.id not in completed_subjects and len(student_allocations[student]) < subjects_to_taught:
                    student_allocations[student].append(potential_subject.subject.name)

        # Save the allocated subjects to the database
        for student, allocated_subjects in student_allocations.items():
            AllocatedSubject.objects.create(student=student, allocated_subjects=allocated_subjects)

        self.stdout.write(self.style.SUCCESS('Successfully allocated subjects to students'))
