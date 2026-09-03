from django import forms

from apps.applications.models import Application
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks.

    The application field is optional because a task can be
    either application-specific or a general task.
    """

    class Meta:
        model = Task
        fields = [
            "application",
            "title",
            "description",
            "due_date",
            "priority",
            "status",
        ]
        widgets = {
            "application": forms.Select(
                attrs={"class": "form-control"}
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Finalize study plan",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Add details about this task...",
                }
            ),
            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "priority": forms.Select(
                attrs={"class": "form-control"}
            ),
            "status": forms.Select(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["application"].queryset = (
            Application.objects
            .filter(user=user)
            .select_related("university", "program")
            .order_by("university__name", "program__name")
        )

        self.fields["application"].required = False

        self.fields["application"].empty_label = "General task"

    def clean_title(self):
        title = " ".join(
            self.cleaned_data["title"].strip().split()
        )

        if not title:
            raise forms.ValidationError(
                "Task title cannot be empty."
            )

        return title