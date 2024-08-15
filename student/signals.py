from .models import UploadStudent, CompletedSubject, Student
from subject.models import Subject

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Student)
def populate_completed_subjects(sender, instance, created, **kwargs):
    if created and instance.completed_subjects:
        for subject_id in instance.completed_subjects:
            try:
                subject = Subject.objects.get(id=subject_id)
                CompletedSubject.objects.get_or_create(
                    student=instance,
                    subject=subject,
                    defaults={'completion_date': None}
                )
            except Subject.DoesNotExist:
                # Log or handle the case where the subject ID does not exist
                pass


