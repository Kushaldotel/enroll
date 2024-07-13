# # In teacher/signals.py

# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Group
# from .models import Teacher
# from django.contrib.auth import get_user_model

# User = get_user_model()

# @receiver(pre_save, sender=Teacher)
# def create_user_for_teacher(sender, instance, **kwargs):
#     if not instance.user_id:
#         user = User.objects.create_user(
#             username=instance.unique_username,
#             password=instance.dob.strftime('%Y-%m-%d'),
#             email=instance.email,
#             first_name=instance.first_name,
#             last_name=instance.last_name
#         )
#         instance.user = user

#         # Add user to 'teacher' group
#         teacher_group, created = Group.objects.get_or_create(name='Teacher')
#         teacher_group.user_set.add(user)
