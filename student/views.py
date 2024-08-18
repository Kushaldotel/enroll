from django.shortcuts import render, redirect
from django import forms
import pandas as pd
from .models import Student, Subject, CompletedSubject

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            df = pd.read_csv(csv_file)

            for _, row in df.iterrows():
                unique_username = row['Student']
                student, _ = Student.objects.get_or_create(unique_username=unique_username)

                for subject_code in df.columns[1:]:
                    status = row[subject_code]
                    subject, _ = Subject.objects.get_or_create(code=subject_code)
                    if status in ['P', 'C', 'E', 'CR', 'CPL']:
                        CompletedSubject.objects.get_or_create(student=student, subject=subject)

            return redirect('upload_success')
    else:
        form = CSVUploadForm()

    return render(request, 'student/upload_csv.html', {'form': form})

def upload_success(request):
    return render(request, 'student/upload_success.html')
