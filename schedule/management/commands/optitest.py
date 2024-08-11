from django.core.management.base import BaseCommand
from student.models import Student
from subject.models import Subject, SubjectToTaught, AllocatedSubject, NewPotentialSubject
from student.models import CompletedSubject
from collections import defaultdict, Counter
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

        # Step 1: Calculate remaining subjects for each student
        student_subjects = {}
        for student in all_students:
            completed_subjects = CompletedSubject.objects.filter(student=student).values_list('subject', flat=True)
            remaining_subjects = list(all_subjects.exclude(id__in=completed_subjects).values_list('name', flat=True))
            student_subjects[student.id] = remaining_subjects

        # Step 2: Identify common subjects among all students
        common_subjects = set(student_subjects[next(iter(student_subjects))])
        for subjects in student_subjects.values():
            common_subjects &= set(subjects)
        common_subjects = sorted(common_subjects)

        # Initialize subjects to be taught list with common subjects
        subjects_to_taught = list(common_subjects)

        # Step 3: Count how many students need each subject and sort by priority
        subject_counter = Counter([subject for subjects in student_subjects.values() for subject in subjects])
        priority_subjects = sorted(subject_counter.keys(), key=lambda x: subject_counter[x], reverse=True)

        # Step 4: Sort students by the number of remaining subjects (highest to lowest)
        sorted_students = sorted(student_subjects.keys(), key=lambda x: len(student_subjects[x]), reverse=True)

        # Step 5: Allocate subjects to each student
        student_allocations = defaultdict(list)

        for student_id in sorted_students:
            allocation = []
            remaining_subjects = student_subjects[student_id]

            # Allocate common subjects first if they are in subjects_to_taught
            for subject in subjects_to_taught:
                if subject in remaining_subjects and subject not in allocation and len(allocation) < subjects_to_allocate:
                    allocation.append(subject)

            # Allocate remaining subjects based on priority and existing subjects_to_taught
            for subject in priority_subjects:
                if subject in remaining_subjects and subject in subjects_to_taught and subject not in allocation and len(allocation) < subjects_to_allocate:
                    allocation.append(subject)

            # Allocate remaining subjects if the limit is not reached
            for subject in priority_subjects:
                if subject in remaining_subjects and subject not in allocation and len(allocation) < subjects_to_allocate:
                    allocation.append(subject)
                    if subject not in subjects_to_taught:
                        subjects_to_taught.append(subject)

            student_allocations[student_id] = allocation

        # Step 6: Store the subjects to be taught by the college
        SubjectToTaught.objects.create(
            subject_names=subjects_to_taught,
            number_of_subjects=len(subjects_to_taught)
        )

        # Step 7: Store the allocated subjects for each student
        for student_id, subjects in student_allocations.items():
            student = Student.objects.get(id=student_id)
            AllocatedSubject.objects.create(
                student=student,
                allocated_subjects=subjects
            )

        # Step 8: Calculate and store remaining students for each subject to be taught
        for subject_name in subjects_to_taught:
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

        self.stdout.write(self.style.SUCCESS(f'Successfully calculated and stored subjects to be taught: {list(subjects_to_taught)}'))
        self.stdout.write(self.style.SUCCESS(f'Student Allocations: {json.dumps(student_allocations, indent=2)}'))
