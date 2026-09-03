from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.applications.models import Application

from .forms import TaskForm
from .models import Task


@login_required
def task_list(request):
    """
    Display the user's tasks with optional filters.
    """

    tasks = (
        Task.objects
        .filter(user=request.user)
        .select_related(
            "application",
            "application__university",
            "application__program",
        )
    )

    status = request.GET.get("status")
    priority = request.GET.get("priority")
    application_id = request.GET.get("application")
    overdue = request.GET.get("overdue")

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    if application_id:
        tasks = tasks.filter(
            application_id=application_id
        )

    if overdue == "1":
        tasks = tasks.filter(
            due_date__lt=timezone.localdate()
        ).exclude(
            status__in=[
                Task.Status.COMPLETED,
                Task.Status.CANCELLED,
            ]
        )

    applications = (
        request.user.applications
        .select_related("university", "program")
        .order_by(
            "university__name",
            "program__name",
        )
    )

    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": tasks,
            "applications": applications,
            "status_choices": Task.Status.choices,
            "priority_choices": Task.Priority.choices,
            "current_status": status,
            "current_priority": priority,
            "current_application": application_id,
            "show_overdue": overdue == "1",
        },
    )


@login_required
def task_create(request, application_id=None):
    """
    Create a new task.

    When an application ID is provided, the task is automatically
    associated with that application.
    """

    application = None

    if application_id is not None:
        application = get_object_or_404(
            Application,
            id=application_id,
            user=request.user,
        )

    if request.method == "POST":
        form = TaskForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user

            if application is not None:
                task.application = application

            task.save()

            messages.success(
                request,
                "Task created successfully.",
            )

            return redirect(
                "tasks:detail",
                task_id=task.id,
            )
    else:
        form = TaskForm(
            user=request.user,
            initial={
                "application": application,
            },
        )

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "application": application,
            "page_title": "Add Task",
            "submit_label": "Create Task",
        },
    )


@login_required
def task_detail(request, task_id):
    """
    Display a single task.
    """

    task = get_object_or_404(
        Task.objects.select_related(
            "application",
            "application__university",
            "application__program",
        ),
        id=task_id,
        user=request.user,
    )

    return render(
        request,
        "tasks/task_detail.html",
        {"task": task},
    )


@login_required
def task_update(request, task_id):
    """
    Update an existing task.
    """

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user,
    )

    if request.method == "POST":
        form = TaskForm(
            request.POST,
            instance=task,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Task updated successfully.",
            )

            return redirect(
                "tasks:detail",
                task_id=task.id,
            )
    else:
        form = TaskForm(
            instance=task,
            user=request.user,
        )

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "task": task,
            "page_title": "Edit Task",
            "submit_label": "Save Changes",
        },
    )


@login_required
def task_delete(request, task_id):
    """
    Delete a task after confirmation.
    """

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user,
    )

    if request.method == "POST":
        task.delete()

        messages.success(
            request,
            "Task deleted successfully.",
        )

        return redirect("tasks:list")

    return render(
        request,
        "tasks/task_confirm_delete.html",
        {"task": task},
    )