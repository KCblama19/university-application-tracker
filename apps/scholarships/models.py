from django.db import models


class Scholarship(models.Model):
    """
    Represents a scholarship or funding opportunity.

    A scholarship is kept independent from a university because
    the same scholarship can potentially be used when applying
    to multiple universities.
    """

    class ScholarshipType(models.TextChoices):
        GOVERNMENT = "GOVERNMENT", "Government"
        UNIVERSITY = "UNIVERSITY", "University"
        PROVINCIAL = "PROVINCIAL", "Provincial"
        PRIVATE = "PRIVATE", "Private"
        OTHER = "OTHER", "Other"

    name = models.CharField(
        max_length=255,
    )

    provider = models.CharField(
        max_length=255,
        blank=True,
        help_text="Organization or institution providing the scholarship.",
    )

    scholarship_type = models.CharField(
        max_length=20,
        choices=ScholarshipType.choices,
        default=ScholarshipType.OTHER,
    )

    deadline = models.DateField(
        null=True,
        blank=True,
    )

    coverage = models.TextField(
        blank=True,
        help_text="What expenses the scholarship covers.",
    )

    stipend = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monthly stipend, if applicable.",
    )

    eligibility = models.TextField(
        blank=True,
    )

    application_url = models.URLField(
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
        ordering = ["deadline", "name"]

    def __str__(self):
        return self.name