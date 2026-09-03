from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from django.core.exceptions import ValidationError


class Document(models.Model):
    """
    Represents a document stored in the user's document library.

    A document is independent of an application so that the same
    file can be reused for multiple university applications.
    """

    class DocumentType(models.TextChoices):
        PASSPORT = "PASSPORT", "Passport"
        TRANSCRIPT = "TRANSCRIPT", "Transcript"
        CV = "CV", "CV / Resume"
        STUDY_PLAN = "STUDY_PLAN", "Study Plan"
        RECOMMENDATION = "RECOMMENDATION", "Recommendation Letter"
        LANGUAGE_CERTIFICATE = "LANGUAGE_CERTIFICATE", "Language Certificate"
        ENROLLMENT_CERTIFICATE = "ENROLLMENT_CERTIFICATE", "Enrollment Certificate"
        PHYSICAL_EXAMINATION = "PHYSICAL_EXAMINATION", "Physical Examination"
        DIPLOMA = "DIPLOMA", "Diploma"
        ID_PHOTO = "ID_PHOTO", "ID Photo"
        OTHER = "OTHER", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    name = models.CharField(
        max_length=255,
        help_text="A name that helps you identify this document.",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )

    file = models.FileField(
        upload_to="documents/%Y/%m/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "jpg",
                    "jpeg",
                    "png",
                ]
            )
        ],
    )

    issue_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    

class ApplicationDocument(models.Model):
    """
    Represents a document requirement for a specific application.

    A requirement can exist before the actual file is available.
    Once the user has the required document, it can be linked here
    from the reusable document library.
    """

    class Status(models.TextChoices):
        NOT_STARTED = "NOT_STARTED", "Not Started"
        READY = "READY", "Ready"
        SUBMITTED = "SUBMITTED", "Submitted"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="application_documents",
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="application_documents",
    )

    document_type = models.CharField(
        max_length=30,
        choices=Document.DocumentType.choices,
    )

    required = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["required", "document_type"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "application",
                    "document",
                    "document_type",
                ],
                condition=models.Q(document__isnull=False),
                name="unique_application_document",
            ),
            models.UniqueConstraint(
                fields=[
                    "application",
                    "document_type",
                ],
                condition=models.Q(document__isnull=True),
                name="unique_application_document_requirement",
            ),
        ]

    def clean(self):
        """
        Validate the relationship between the application,
        the selected document, and the document type.
        """

        super().clean()

        if self.document_id:
            if self.document.user_id != self.application.user_id:
                raise ValidationError(
                    {
                        "document": (
                            "The selected document does not belong "
                            "to this application owner."
                        )
                    }
                )

            if self.document.document_type != self.document_type:
                raise ValidationError(
                    {
                        "document_type": (
                            "The document type must match the "
                            "selected document."
                        )
                    }
                )

        if (
            self.status
            in {
                self.Status.READY,
                self.Status.SUBMITTED,
                self.Status.VERIFIED,
            }
            and not self.document_id
        ):
            raise ValidationError(
                {
                    "document": (
                        "A document must be attached before "
                        "using this status."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.application} — "
            f"{self.get_document_type_display()}"
        )