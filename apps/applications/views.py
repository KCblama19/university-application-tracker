from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm
from .models import Application
from apps.universities.models import Program


@login_required
def application_list(request):
    """
    Display applications belonging to the currently logged-in user.
    """
    applications = (
        Application.objects
        .filter(user=request.user)
        .select_related("university", "program", "scholarship")
    )

    return render(
        request,
        "applications/application_list.html",
        {
            "applications": applications,
        },
    )


@login_required
def application_detail(request, application_id):
    """
    Display an application and its related records.
    """
    application = get_object_or_404(
        Application.objects
        .select_related(
            "university",
            "program",
            "scholarship",
        )
        .prefetch_related(
            "application_documents__document",
            "tasks",
            "contacts",
        ),
        id=application_id,
        user=request.user,
    )

    return render(
        request,
        "applications/application_detail.html",
        {
            "application": application,
        },
    )


@login_required
def application_create(request):
    """
    Create a new application for the currently logged-in user.
    """
    if request.method == "POST":
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()

            messages.success(
                request,
                "Application created successfully.",
            )

            return redirect(
                "applications:detail",
                application_id=application.id,
            )
    else:
        form = ApplicationForm()

    return render(
        request,
        "applications/application_form.html",
        {
            "form": form,
            "page_title": "Add Application",
            "submit_label": "Create Application",
        },
    )


@login_required
def application_update(request, application_id):
    """
    Update an application belonging to the currently logged-in user.
    """
    application = get_object_or_404(
        Application,
        id=application_id,
        user=request.user,
    )

    if request.method == "POST":
        form = ApplicationForm(
            request.POST,
            instance=application,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Application updated successfully.",
            )

            return redirect(
                "applications:detail",
                application_id=application.id,
            )
    else:
        form = ApplicationForm(instance=application)

    return render(
        request,
        "applications/application_form.html",
        {
            "form": form,
            "application": application,
            "page_title": "Edit Application",
            "submit_label": "Save Changes",
        },
    )


@login_required
def application_delete(request, application_id):
    """
    Delete an application belonging to the currently logged-in user.
    """
    application = get_object_or_404(
        Application,
        id=application_id,
        user=request.user,
    )

    if request.method == "POST":
        application.delete()

        messages.success(
            request,
            "Application deleted successfully.",
        )

        return redirect("applications:list")

    return render(
        request,
        "applications/application_confirm_delete.html",
        {
            "application": application,
        },
    )


@login_required
def university_programs(request, university_id):
    """
    Return programs belonging to a selected university.

    This endpoint is used by the application form to populate
    the program dropdown dynamically.
    """
    programs = (
        Program.objects
        .filter(university_id=university_id)
        .order_by("name")
    )

    data = [
        {
            "id": program.id,
            "name": program.name,
        }
        for program in programs
    ]

    return JsonResponse(data, safe=False)
