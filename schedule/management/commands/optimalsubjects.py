# schedule/management/commands/subjectstaught.py

from django.core.management.base import BaseCommand
from student.models import Student
from subject.models import Subject, SubjectToTaught, AllocatedSubject, NewPotentialSubject
from student.models import CompletedSubject
from collections import defaultdict
import json

class Command(BaseCommand):
    help = 'Calculate and store subjects to be taught by the college'

    def handle(self, *args, **kwargs):
        subjects_to_allocate = 4  # Number of subjects to allocate

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
            student_subjects[student.id] = sorted(remaining_subjects.values_list('name', flat=True))

        # Step 1: Find common subjects among all students
        if student_subjects:
            common_subjects = set(student_subjects[next(iter(student_subjects))])
            for subjects in student_subjects.values():
                common_subjects &= set(subjects)
            common_subjects = sorted(common_subjects)
        else:
            common_subjects = []

        # Step 2: Allocate common subjects to each student
        subjects_to_be_taught = common_subjects[:]
        student_allocations = defaultdict(list)
        remaining_subjects_pool = set()

        for student_id, remaining_subjects in student_subjects.items():
            allocation = [subject for subject in common_subjects if subject in remaining_subjects][:subjects_to_allocate]
            remaining_subjects_pool.update(set(remaining_subjects) - set(allocation))
            student_allocations[student_id] = allocation

        # Step 3: Fill remaining allocations to ensure 4 subjects per student
        for student_id, allocation in student_allocations.items():
            remaining_subjects = [subject for subject in student_subjects[student_id] if subject not in allocation]
            while len(allocation) < subjects_to_allocate and remaining_subjects:
                subject_to_add = remaining_subjects.pop(0)
                if subject_to_add not in allocation:
                    allocation.append(subject_to_add)
                    if subject_to_add not in subjects_to_be_taught:
                        subjects_to_be_taught.append(subject_to_add)
            student_allocations[student_id] = allocation

        # Step 4: Store the subjects to be taught by the college
        SubjectToTaught.objects.create(
            subject_names=subjects_to_be_taught,
            number_of_subjects=len(subjects_to_be_taught)
        )

        # Step 5: Store the allocated subjects for each student
        for student_id, subjects in student_allocations.items():
            student = Student.objects.get(id=student_id)
            AllocatedSubject.objects.create(
                student=student,
                allocated_subjects=subjects
            )

        # Step 6: Calculate and store remaining students for each subject to be taught
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

# Running this command will now consistently allocate subjects and calculate the optimal solution based on your requirements.
