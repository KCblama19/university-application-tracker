from django.conf import settings
from django.db import models

from django.core.exceptions import ValidationError


class Contact(models.Model):
    """
    Represents a university contact, such as a professor,
    department coordinator, admissions officer, or supervisor.

    A contact belongs to a university and can optionally be
    associated with a specific application.
    """

    class Status(models.TextChoices):
        NOT_CONTACTED = "NOT_CONTACTED", "Not Contacted"
        EMAIL_SENT = "EMAIL_SENT", "Email Sent"
        RESPONDED = "RESPONDED", "Responded"
        FOLLOW_UP = "FOLLOW_UP", "Follow Up"
        NO_RESPONSE = "NO_RESPONSE", "No Response"
        NOT_INTERESTED = "NOT_INTERESTED", "Not Interested"
        POSITIVE = "POSITIVE", "Positive Response"
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    
    university = models.ForeignKey(
        "universities.University",
        on_delete=models.PROTECT,
        related_name="contacts",
    )

    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.SET_NULL,
        related_name="contacts",
        null=True,
        blank=True,
        help_text="Optional application this contact is associated with.",
    )

    name = models.CharField(
        max_length=255,
    )

    position = models.CharField(
        max_length=255,
        blank=True,
        help_text="For example: Professor, Associate Professor, Admissions Officer.",
    )

    department = models.CharField(
        max_length=255,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    research_area = models.CharField(
        max_length=500,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_CONTACTED,
    )

    last_contacted = models.DateField(
        null=True,
        blank=True,
    )

    follow_up_date = models.DateField(
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
    
    def clean(self):
        """
        Validate that an associated application belongs to
        the same university and user as the contact.
        """
        super().clean()

        if self.application_id:
            if self.application.university_id != self.university_id:
                raise ValidationError(
                    {
                        "application": (
                            "The selected application does not belong "
                            "to this university."
                        )
                    }
                )

            if self.application.user_id != self.user_id:
                raise ValidationError(
                    {
                        "application": (
                            "The selected application does not belong "
                            "to this user."
                        )
                    }
                )

    class Meta:
        ordering = ["-updated_at", "name"]

    def __str__(self):
        return f"{self.name} — {self.university.name}"