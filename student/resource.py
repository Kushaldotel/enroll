from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import CompletedSubject, Subject, Student

class CompletedSubjectResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='id')
    student_id = fields.Field(attribute='student', column_name='student_id')
    subject_code = fields.Field(attribute='subject', column_name='subject_code')

    class Meta:
        model = CompletedSubject
        fields = ('id', 'student_id', 'subject_code')
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

    def dehydrate_subject_code(self, completed_subject):
        return completed_subject.subject.code

    def hydrate_subject_code(self, subject_code):
        try:
            subject = Subject.objects.get(code=subject_code)
            return subject
        except Subject.DoesNotExist:
            raise ValueError(f"Subject with code '{subject_code}' does not exist.")

    def dehydrate_student_id(self, completed_subject):
        return completed_subject.student.id

    def hydrate_student_id(self, student_id):
        try:
            student = Student.objects.get(id=student_id)
            return student
        except Student.DoesNotExist:
            raise ValueError(f"Student with ID '{student_id}' does not exist.")
