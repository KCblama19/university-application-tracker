from django import forms

from .models import Scholarship


class ScholarshipForm(forms.ModelForm):
    """
    Form for creating and editing scholarship opportunities.
    """

    class Meta:
        model = Scholarship

        fields = [
            "name",
            "provider",
            "scholarship_type",
            "deadline",
            "coverage",
            "stipend",
            "eligibility",
            "application_url",
            "notes",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Chinese Government Scholarship",
                }
            ),
            "provider": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. China Scholarship Council",
                }
            ),
            "scholarship_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "coverage": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "What expenses does the scholarship cover?",
                }
            ),
            "stipend": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "e.g. 3000",
                }
            ),
            "eligibility": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Who is eligible for this scholarship?",
                }
            ),
            "application_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://...",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Add notes about this scholarship...",
                }
            ),
        }

    def clean_name(self):
        name = " ".join(
            self.cleaned_data["name"].strip().split()
        )

        if not name:
            raise forms.ValidationError(
                "Scholarship name cannot be empty."
            )

        return name

    def clean_stipend(self):
        stipend = self.cleaned_data.get("stipend")

        if stipend is not None and stipend < 0:
            raise forms.ValidationError(
                "Stipend cannot be negative."
            )

        return stipend