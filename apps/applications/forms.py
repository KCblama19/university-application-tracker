from django import forms

from .models import Application
from apps.scholarships.models import Scholarship
from apps.universities.models import University, Program


class ApplicationForm(forms.ModelForm):
    """
    Form used to create and update university applications.

    The program choices are filtered based on the selected university
    so that users cannot accidentally associate an application with
    a program belonging to another university.
    """

    class Meta:
        model = Application
        fields = [
            "university",
            "program",
            "scholarship",
            "status",
            "application_deadline",
            "scholarship_deadline",
            "portal_url",
            "submitted_at",
            "decision_at",
            "notes",
        ]

        widgets = {
            "university": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "program": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "scholarship": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "application_deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "scholarship_deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "portal_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://...",
                }
            ),
            "submitted_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "decision_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Add notes about this application...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Start with no programs displayed.
        # Programs will be populated after a university is selected.
        self.fields["program"].queryset = Program.objects.none()

        # When editing an existing application, populate the program
        # field with programs belonging to its university.
        if self.instance.pk and self.instance.university_id:
            self.fields["program"].queryset = Program.objects.filter(
                university=self.instance.university
            )

        # Keep scholarship choices predictable and ordered.
        self.fields["scholarship"].queryset = Scholarship.objects.order_by(
            "name"
        )

        self.fields["university"].queryset = University.objects.order_by(
            "name"
        )

    def clean(self):
        """
        Validate relationships and status-dependent application dates.
        """
        cleaned_data = super().clean()

        university = cleaned_data.get("university")
        program = cleaned_data.get("program")

        if university and program:
            if program.university_id != university.id:
                self.add_error(
                    "program",
                    "The selected program does not belong to the selected university.",
                )

        status = cleaned_data.get("status")
        submitted_at = cleaned_data.get("submitted_at")
        decision_at = cleaned_data.get("decision_at")

        submitted_statuses = {
            Application.Status.SUBMITTED,
            Application.Status.UNDER_REVIEW,
            Application.Status.INTERVIEW,
            Application.Status.ACCEPTED,
            Application.Status.REJECTED,
        }

        final_statuses = {
            Application.Status.ACCEPTED,
            Application.Status.REJECTED,
        }

        if status in submitted_statuses and not submitted_at:
            self.add_error(
                "submitted_at",
                "Enter the submission date before using this status.",
            )

        if status in final_statuses and not decision_at:
            self.add_error(
                "decision_at",
                "Enter the decision date for an accepted or rejected application.",
            )

        if status not in final_statuses and decision_at:
            self.add_error(
                "decision_at",
                "A decision date should only be provided for an accepted or rejected application.",
            )

        if submitted_at and decision_at and decision_at < submitted_at:
            self.add_error(
                "decision_at",
                "The decision date cannot be earlier than the submission date.",
            )

        return cleaned_data