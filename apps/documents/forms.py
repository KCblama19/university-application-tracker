from django import forms

from .models import Document, ApplicationDocument


class DocumentForm(forms.ModelForm):
    """
    Form for adding and editing documents in the user's
    personal document library.
    """

    class Meta:
        model = Document
        fields = [
            "name",
            "document_type",
            "file",
            "issue_date",
            "expiry_date",
            "notes",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Bachelor's Transcript",
                }
            ),
            "document_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "issue_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "expiry_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Add notes about this document...",
                }
            ),
        }

    def clean_name(self):
        """
        Normalize whitespace in the document name.
        """
        return " ".join(self.cleaned_data["name"].strip().split())

    def clean(self):
        """
        Ensure an expiry date is not earlier than the issue date.
        """
        cleaned_data = super().clean()

        issue_date = cleaned_data.get("issue_date")
        expiry_date = cleaned_data.get("expiry_date")

        if issue_date and expiry_date and expiry_date < issue_date:
            self.add_error(
                "expiry_date",
                "Expiry date cannot be earlier than the issue date.",
            )

        return cleaned_data
    

class ApplicationDocumentForm(forms.ModelForm):
    """
    Form for creating and updating an application document
    requirement.

    A requirement can be created without an uploaded document.
    The actual file can be attached later from the user's
    document library.
    """

    class Meta:
        model = ApplicationDocument

        fields = [
            "document_type",
            "document",
            "required",
            "status",
            "submitted_at",
            "notes",
        ]

        widgets = {
            "document_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "document": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "required": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "submitted_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Add notes about this application "
                        "document..."
                    ),
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["document"].queryset = (
            Document.objects
            .filter(user=user)
            .order_by("name")
        )

        self.fields["document"].required = False

    def clean(self):
        cleaned_data = super().clean()

        document = cleaned_data.get("document")
        document_type = cleaned_data.get("document_type")
        status = cleaned_data.get("status")

        if document:
            if document.document_type != document_type:
                self.add_error(
                    "document_type",
                    (
                        "The document type must match "
                        "the selected document."
                    ),
                )

        if (
            status
            in {
                ApplicationDocument.Status.READY,
                ApplicationDocument.Status.SUBMITTED,
                ApplicationDocument.Status.VERIFIED,
            }
            and not document
        ):
            self.add_error(
                "document",
                (
                    "Attach a document before marking this "
                    "requirement as ready, submitted, or verified."
                ),
            )

        return cleaned_data