# In teacher/models.py

from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    unique_username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    temporary_address = models.TextField()
    permanent_address = models.TextField()

    department = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
