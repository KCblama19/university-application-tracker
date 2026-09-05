from django.db import models

class University(models.Model):
    """
    Represents a university that the user is researching
    or considering for an application.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    country = models.CharField(
        max_length=100,
        default="China",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    ranking = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Optional overall ranking used for personal comparison.",
    )

    description = models.TextField(
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
    
    constraints = [
        models.UniqueConstraint(
            fields=["university", "name", "degree_type"],
            name="unique_program_per_university_degree",
        ),
        models.CheckConstraint(
            condition=models.Q(duration__gte=0) | models.Q(duration__isnull=True),
            name="program_duration_non_negative",
        ),
        models.CheckConstraint(
            condition=models.Q(tuition_fee__gte=0) | models.Q(tuition_fee__isnull=True),
            name="program_tuition_non_negative",
        ),
    ]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Program(models.Model):
    """
    Represents a specific academic program offered by a university.

    A university can offer many programs.
    """

    class DegreeType(models.TextChoices):
        BACHELOR = "BACHELOR", "Bachelor's"
        MASTER = "MASTER", "Master's"
        PHD = "PHD", "PhD"

    class StudyLanguage(models.TextChoices):
        ENGLISH = "ENGLISH", "English"
        CHINESE = "CHINESE", "Chinese"
        BILINGUAL = "BILINGUAL", "Bilingual"
        OTHER = "OTHER", "Other"

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="programs",
    )

    name = models.CharField(
        max_length=255,
    )

    degree_type = models.CharField(
        max_length=20,
        choices=DegreeType.choices,
    )

    study_language = models.CharField(
        max_length=20,
        choices=StudyLanguage.choices,
        default=StudyLanguage.ENGLISH,
    )

    duration = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Program duration in years.",
    )

    tuition_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Annual tuition fee.",
    )

    description = models.TextField(
        blank=True,
    )

    requirements = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["university__name", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["university", "name", "degree_type"],
                name="unique_program_per_university_degree",
            ),
        ]

    def __str__(self):
        return f"{self.name} — {self.university.name}"