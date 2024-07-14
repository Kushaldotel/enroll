# In schedule/management/commands/subjectstaught.py

from django.core.management.base import BaseCommand
from student.models import Student
from subject.models import Subject, SubjectToTaught, AllocatedSubject, NewPotentialSubject
from student.models import CompletedSubject
from collections import defaultdict
import json

class Command(BaseCommand):
    help = 'Calculate and store subjects to be taught by the college'

    def handle(self, *args, **kwargs):
        subjects_to_allocate = 4  # Explicitly define the number of subjects to allocate

        # Clear existing SubjectToTaught, AllocatedSubject, and NewPotentialSubject data
        SubjectToTaught.objects.all().delete()
        AllocatedSubject.objects.all().delete()
        NewPotentialSubject.objects.all().delete()

        # Get all students and subjects
        all_students = Student.objects.all()
        all_subjects = Subject.objects.all()

        # Calculate remaining subjects for each student
        student_subjects = {}
        for student in all_students:
            completed_subjects = CompletedSubject.objects.filter(student=student).values_list('subject', flat=True)
            remaining_subjects = all_subjects.exclude(id__in=completed_subjects)
            student_subjects[student.id] = set(remaining_subjects.values_list('name', flat=True))

        # Find common subjects among all students
        common_subjects = set.intersection(*student_subjects.values()) if student_subjects else set()

        # Collect required subjects
        required_subjects = set()
        student_allocations = defaultdict(list)

        for student_id, remaining_subjects in student_subjects.items():
            allocation = list(common_subjects & remaining_subjects)[:subjects_to_allocate]
            remaining = list(remaining_subjects - common_subjects)[:subjects_to_allocate - len(allocation)]
            student_allocations[student_id] = allocation + remaining
            required_subjects.update(allocation + remaining)

        # Store the subjects to be taught by the college
        subjects_to_be_taught = list(required_subjects)
        SubjectToTaught.objects.create(
            subject_names=subjects_to_be_taught,
            number_of_subjects=len(subjects_to_be_taught)
        )

        # Store the allocated subjects for each student
        for student_id, subjects in student_allocations.items():
            student = Student.objects.get(id=student_id)
            AllocatedSubject.objects.create(
                student=student,
                allocated_subjects=subjects
            )

        # Calculate and store remaining students for each subject to be taught
        for subject_name in subjects_to_be_taught:
            subject = Subject.objects.get(name=subject_name)
            remaining_students = []
            for student in all_students:
                completed_subjects = CompletedSubject.objects.filter(student=student).values_list('subject', flat=True)
                if subject.id not in completed_subjects:
                    remaining_students.append(student.first_name)
            if remaining_students:
                NewPotentialSubject.objects.create(
                    subject=subject,
                    remaining_students=len(remaining_students),
                    remaining_student_names=remaining_students
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully calculated and stored subjects to be taught: {subjects_to_be_taught}'))
        self.stdout.write(self.style.SUCCESS(f'Student Allocations: {json.dumps(student_allocations, indent=2)}'))
