from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from apps.applications.models import Application
from apps.documents.models import ApplicationDocument
from apps.scholarships.models import Scholarship
from apps.tasks.models import Task


@login_required
def home(request):
    """
    Display the application tracker dashboard.

    The dashboard aggregates information from the existing
    application, document, scholarship, and task models.
    """

    today = timezone.localdate()
    upcoming_limit = today + timedelta(days=30)

    applications = (
        Application.objects
        .filter(user=request.user)
        .select_related(
            "university",
            "program",
            "scholarship",
        )
    )

    tasks = (
        Task.objects
        .filter(user=request.user)
        .select_related(
            "application",
            "application__university",
            "application__program",
        )
    )

    # ------------------------------------------------------------------
    # Application statistics
    # ------------------------------------------------------------------

    total_applications = applications.count()

    submitted_applications = applications.filter(
        status__in=[
            Application.Status.SUBMITTED,
            Application.Status.UNDER_REVIEW,
            Application.Status.INTERVIEW,
            Application.Status.ACCEPTED,
            Application.Status.REJECTED,
        ]
    ).count()

    in_progress_applications = applications.filter(
        status__in=[
            Application.Status.RESEARCHING,
            Application.Status.SHORTLISTED,
            Application.Status.PREPARING,
            Application.Status.APPLICATION_STARTED,
        ]
    ).count()

    # ------------------------------------------------------------------
    # Upcoming application deadlines
    # ------------------------------------------------------------------

    upcoming_applications = (
        applications
        .filter(
            application_deadline__isnull=False,
            application_deadline__gte=today,
            application_deadline__lte=upcoming_limit,
        )
        .order_by("application_deadline")[:5]
    )

    upcoming_deadlines = applications.filter(
        application_deadline__isnull=False,
        application_deadline__gte=today,
        application_deadline__lte=upcoming_limit,
    ).count()

    # ------------------------------------------------------------------
    # Task statistics
    # ------------------------------------------------------------------

    pending_tasks = (
        tasks
        .exclude(
            status__in=[
                Task.Status.COMPLETED,
                Task.Status.CANCELLED,
            ]
        )
        .order_by("due_date", "-priority")[:5]
    )

    overdue_tasks = tasks.filter(
        due_date__lt=today,
    ).exclude(
        status__in=[
            Task.Status.COMPLETED,
            Task.Status.CANCELLED,
        ]
    ).count()

    pending_task_count = tasks.exclude(
        status__in=[
            Task.Status.COMPLETED,
            Task.Status.CANCELLED,
        ]
    ).count()

    # ------------------------------------------------------------------
    # Document statistics
    # ------------------------------------------------------------------

    application_documents = ApplicationDocument.objects.filter(
        application__user=request.user,
    )

    total_document_requirements = application_documents.count()

    completed_document_requirements = application_documents.filter(
        status__in=[
            ApplicationDocument.Status.SUBMITTED,
            ApplicationDocument.Status.VERIFIED,
        ]
    ).count()

    pending_document_requirements = application_documents.exclude(
        status__in=[
            ApplicationDocument.Status.SUBMITTED,
            ApplicationDocument.Status.VERIFIED,
        ]
    ).count()

    # ------------------------------------------------------------------
    # Scholarship deadlines
    # ------------------------------------------------------------------

    upcoming_scholarships = (
        Scholarship.objects
        .filter(
            deadline__isnull=False,
            deadline__gte=today,
            deadline__lte=upcoming_limit,
        )
        .order_by("deadline", "name")[:5]
    )

    # ------------------------------------------------------------------
    # Application status breakdown
    # ------------------------------------------------------------------

    application_status_counts = (
        applications
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    context = {
        "total_applications": total_applications,
        "submitted_applications": submitted_applications,
        "in_progress_applications": in_progress_applications,

        "upcoming_deadlines": upcoming_deadlines,
        "upcoming_applications": upcoming_applications,

        "pending_tasks": pending_tasks,
        "pending_task_count": pending_task_count,
        "overdue_tasks": overdue_tasks,

        "total_document_requirements": total_document_requirements,
        "completed_document_requirements": completed_document_requirements,
        "pending_document_requirements": pending_document_requirements,

        "upcoming_scholarships": upcoming_scholarships,

        "application_status_counts": application_status_counts,
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )