from student.models import CompletedSubject

from django.core.management.base import BaseCommand

from student.models import Student

class Command(BaseCommand):
    help = 'Calculate and store potential subjects along with the number of students remaining to study them'

    def handle(self, *args, **kwargs):

        subjects = CompletedSubject.objects.all()

        #delete each instance of the model

        for subject in subjects:
            subject.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted'))