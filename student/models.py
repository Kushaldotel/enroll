from django.db import models
from django.contrib.auth.models import Group, User
from subject.models import Subject

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    unique_username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=35)
    temporary_address = models.TextField()
    permanent_address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CompletedSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} completed {self.subject} on {self.completion_date}"

    class Meta:
        unique_together = ('student', 'subject')
