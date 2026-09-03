from django.conf import settings
from django.db import models

from django.core.exceptions import ValidationError
from django.utils import timezone


class Application(models.Model):
    """
    Represents one application to a specific academic program
    at a university.

    An application belongs to a user and connects that user to:
        - a university
        - a specific program
        - an optional scholarship

    The application also tracks its current stage, important
    deadlines, submission information, and personal notes.
    """

    class Status(models.TextChoices):
        RESEARCHING = "RESEARCHING", "Researching"
        SHORTLISTED = "SHORTLISTED", "Shortlisted"
        PREPARING = "PREPARING", "Preparing"
        APPLICATION_STARTED = "APPLICATION_STARTED", "Application Started"
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        INTERVIEW = "INTERVIEW", "Interview"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    university = models.ForeignKey(
        "universities.University",
        on_delete=models.PROTECT,
        related_name="applications",
    )

    program = models.ForeignKey(
        "universities.Program",
        on_delete=models.PROTECT,
        related_name="applications",
    )

    scholarship = models.ForeignKey(
        "scholarships.Scholarship",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.RESEARCHING,
    )
    
    status_updated_at = models.DateTimeField(
    null=True,
    blank=True,
    )
    
    application_deadline = models.DateField(
        null=True,
        blank=True,
    )

    scholarship_deadline = models.DateField(
        null=True,
        blank=True,
    )

    portal_url = models.URLField(
        blank=True,
        help_text="Direct URL to the university application portal.",
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    decision_at = models.DateTimeField(
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
        ordering = ["application_deadline", "-created_at"]

        constraints = [
            # Prevent duplicate applications for the same scholarship.
            models.UniqueConstraint(
                fields=[
                    "user",
                    "university",
                    "program",
                    "scholarship",
                ],
                name="unique_user_application_with_scholarship",
                condition=models.Q(scholarship__isnull=False),
            ),

            # Prevent duplicate applications when no scholarship is attached.
            models.UniqueConstraint(
                fields=[
                    "user",
                    "university",
                    "program",
                ],
                name="unique_user_application_without_scholarship",
                condition=models.Q(scholarship__isnull=True),
            ),
        ]

    def __str__(self):
        return f"{self.university.name} — {self.program.name}"

    @property
    def is_submitted(self):
        """
        Returns True when the application has been submitted.
        """
        return self.status in {
            self.Status.SUBMITTED,
            self.Status.UNDER_REVIEW,
            self.Status.INTERVIEW,
            self.Status.ACCEPTED,
            self.Status.REJECTED,
        }
    

    def clean(self):
        """
        Validate relationships between the application,
        university, and program.
        """
        super().clean()

        if self.program_id and self.university_id:
            if self.program.university_id != self.university_id:
                raise ValidationError(
                    {
                        "program": (
                            "The selected program does not belong "
                            "to the selected university."
                        )
                    }
                )
                
    def save(self, *args, **kwargs):
        if self.pk:
            previous = Application.objects.get(pk=self.pk)

            if previous.status != self.status:
                self.status_updated_at = timezone.now()

        elif self.status_updated_at is None:
            self.status_updated_at = timezone.now()

        super().save(*args, **kwargs)