# Generated by Django 5.0.7 on 2024-08-17 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_remove_completedsubject_completion_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedsubject',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
