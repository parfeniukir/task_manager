from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "deadline"]

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        today = timezone.now().date()

        if deadline < today:
            raise forms.ValidationError("Deadline cannot be in the past.")

        return deadline
