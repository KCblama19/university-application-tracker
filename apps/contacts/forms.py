from django import forms

from apps.applications.models import Application
from apps.universities.models import University
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Form for creating and updating university contacts.

    University and application choices are restricted to the
    current user's data.
    """

    class Meta:
        model = Contact
        fields = [
            "university",
            "application",
            "name",
            "position",
            "department",
            "email",
            "research_area",
            "status",
            "last_contacted",
            "follow_up_date",
            "notes",
        ]
        widgets = {
            "university": forms.Select(
                attrs={"class": "form-control"}
            ),
            "application": forms.Select(
                attrs={"class": "form-control"}
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Professor John Doe",
                }
            ),
            "position": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Professor",
                }
            ),
            "department": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. School of Computer Science",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "professor@example.edu",
                }
            ),
            "research_area": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Artificial Intelligence",
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-control"}
            ),
            "last_contacted": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "follow_up_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Add notes about this contact...",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        self.fields["university"].queryset = (
            University.objects.order_by("name")
        )

        self.fields["application"].queryset = (
            Application.objects
            .filter(user=user)
            .select_related("university", "program")
            .order_by(
                "university__name",
                "program__name",
            )
        )

        self.fields["application"].required = False
        self.fields["application"].empty_label = "No specific application"

    def clean_name(self):
        name = " ".join(
            self.cleaned_data["name"].strip().split()
        )

        if not name:
            raise forms.ValidationError(
                "Contact name cannot be empty."
            )

        return name

    def clean(self):
        cleaned_data = super().clean()

        university = cleaned_data.get("university")
        application = cleaned_data.get("application")

        if university and application:
            if application.university_id != university.id:
                self.add_error(
                    "application",
                    "The selected application does not belong to "
                    "the selected university.",
                )

        return cleaned_data