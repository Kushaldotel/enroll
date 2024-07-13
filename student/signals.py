# import re
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User, Group
# from .models import Student

# @receiver(pre_save, sender=Student)
# def create_user_for_student(sender, instance, **kwargs):
#     if not instance.user_id:  # Check if user_id is not set (user object not created)
#         # Create the User object
#         user = User.objects.create_user(
#             username=instance.unique_username,
#             password=instance.dob.strftime('%Y-%m-%d'),
#             email=instance.email,
#             first_name=instance.first_name,
#             last_name=instance.last_name
#         )
#         instance.user = user  # Assign the created user to the student instance

#         # Add the User to the 'student' group
#         student_group, created = Group.objects.get_or_create(name='student')
#         user.groups.add(student_group)
