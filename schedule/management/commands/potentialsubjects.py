# In enrollment/management/commands/potentialsubjects.py

from django.core.management.base import BaseCommand
from student.models import Student
from subject.models import Subject
from subject.models import  PotentialSubject
from student.models import CompletedSubject

# class Command(BaseCommand):
#     help = 'Calculate and store potential subjects along with the number of students remaining to study them'

#     def handle(self, *args, **kwargs):
#         # Clear existing PotentialSubject data
#         PotentialSubject.objects.all().delete()

#         # Get all students and subjects
#         all_students = Student.objects.all()
#         all_subjects = Subject.objects.all()

#         # Calculate the number of students who haven't studied each subject
#         potential_subjects = []

#         for subject in all_subjects:
#             students_completed_subject = CompletedSubject.objects.filter(subject=subject).values_list('student', flat=True)
#             remaining_students_count = all_students.exclude(id__in=students_completed_subject).count()
#             potential_subjects.append((subject, remaining_students_count))

#         # Sort potential subjects by the number of remaining students in descending order
#         potential_subjects.sort(key=lambda x: x[1], reverse=True)

#         # Save potential subjects to the database
#         for subject, remaining_students in potential_subjects:
#             PotentialSubject.objects.create(subject=subject, remaining_students=remaining_students)

#         self.stdout.write(self.style.SUCCESS('Successfully calculated and stored potential subjects'))


class Command(BaseCommand):
    help = 'Calculate and store potential subjects along with the number of students remaining to study them'

    def handle(self, *args, **kwargs):
        # Clear existing PotentialSubject data
        PotentialSubject.objects.all().delete()

        # Get all students and subjects
        all_students = Student.objects.all()
        all_subjects = Subject.objects.all()

        # Calculate the number of students who haven't studied each subject
        potential_subjects = []

        for subject in all_subjects:
            students_completed_subject = CompletedSubject.objects.filter(subject=subject).values_list('student', flat=True)
            remaining_students = all_students.exclude(id__in=students_completed_subject)
            remaining_students_count = remaining_students.count()
            remaining_student_names = [f"{student.first_name} {student.last_name}" for student in remaining_students]

            potential_subjects.append((subject, remaining_students_count, remaining_student_names))

        # Sort potential subjects by the number of remaining students in descending order
        potential_subjects.sort(key=lambda x: x[1], reverse=True)

        # Save potential subjects to the database
        for subject, remaining_students_count, remaining_student_names in potential_subjects:
            PotentialSubject.objects.create(
                subject=subject,
                remaining_students=remaining_students_count,
                remaining_student_names=remaining_student_names
            )

        self.stdout.write(self.style.SUCCESS('Successfully calculated and stored potential subjects'))