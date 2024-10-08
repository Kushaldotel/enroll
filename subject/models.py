from django.db import models
from django.contrib.postgres.fields import ArrayField
class Subject(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class PotentialSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    remaining_students = models.IntegerField()
    remaining_student_names = ArrayField(models.CharField(max_length=255), blank=True, null=True)

    def __str__(self):
        return f"{self.subject} - {self.remaining_students} students remaining"


class SubjectToTaught(models.Model):
    subject_names = ArrayField(models.CharField(max_length=255), default=list)
    number_of_subjects = models.IntegerField()

    # def __str__(self):
    #     return f"Subjects to be taught: {', '.join(self.subject_names)}"

    def __str__(self):
        return f"Subjects to be taught: {self.number_of_subjects}"

class AllocatedSubject(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    allocated_subjects = ArrayField(models.CharField(max_length=255))

    def __str__(self):
        return f"{self.student}: {', '.join(self.allocated_subjects)}"

class NewPotentialSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    remaining_students = models.IntegerField()
    remaining_student_names = ArrayField(models.CharField(max_length=255), blank=True, null=True)

    def __str__(self):
        return f"{self.subject} - {self.remaining_students} students remaining"