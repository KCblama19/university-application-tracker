from django.conf import settings
from django.db import models


class Task(models.Model):
    """
    Represents an action the user needs to complete.

    A task can optionally belong to an application. This allows
    us to have both application-specific tasks and general tasks.
    """

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "status",
            "due_date",
            "-priority",
        ]

    def __str__(self):
        return self.title

    @property
    def is_completed(self):
        """
        Returns True when the task has been completed.
        """
        return self.status == self.Status.COMPLETED

    @property
    def is_overdue(self):
        """
        Returns True when the task has a due date in the past
        and has not yet been completed or cancelled.
        """
        from django.utils import timezone

        if not self.due_date:
            return False

        if self.status in {
            self.Status.COMPLETED,
            self.Status.CANCELLED,
        }:
            return False

        return self.due_date < timezone.localdate()
    
    def save(self, *args, **kwargs):
        """
        Keep completed_at synchronized with the task status.
        """
        from django.utils import timezone

        if self.status == self.Status.COMPLETED:
            if self.completed_at is None:
                self.completed_at = timezone.now()
        else:
            self.completed_at = None

        super().save(*args, **kwargs)