from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ScholarshipForm
from .models import Scholarship


@login_required
def scholarship_list(request):
    """
    Display all scholarships in the user's scholarship tracker.
    """

    scholarships = Scholarship.objects.all()

    return render(
        request,
        "scholarships/scholarship_list.html",
        {
            "scholarships": scholarships,
        },
    )


@login_required
def scholarship_create(request):
    """
    Create a new scholarship opportunity.
    """

    if request.method == "POST":
        form = ScholarshipForm(request.POST)

        if form.is_valid():
            scholarship = form.save()

            messages.success(
                request,
                "Scholarship created successfully.",
            )

            return redirect(
                "scholarships:detail",
                scholarship_id=scholarship.id,
            )
    else:
        form = ScholarshipForm()

    return render(
        request,
        "scholarships/scholarship_form.html",
        {
            "form": form,
            "page_title": "Add Scholarship",
            "submit_label": "Create Scholarship",
        },
    )


@login_required
def scholarship_detail(request, scholarship_id):
    """
    Display detailed information about a scholarship.
    """

    scholarship = get_object_or_404(
        Scholarship,
        id=scholarship_id,
    )

    return render(
        request,
        "scholarships/scholarship_detail.html",
        {
            "scholarship": scholarship,
        },
    )


@login_required
def scholarship_update(request, scholarship_id):
    """
    Edit an existing scholarship.
    """

    scholarship = get_object_or_404(
        Scholarship,
        id=scholarship_id,
    )

    if request.method == "POST":
        form = ScholarshipForm(
            request.POST,
            instance=scholarship,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Scholarship updated successfully.",
            )

            return redirect(
                "scholarships:detail",
                scholarship_id=scholarship.id,
            )
    else:
        form = ScholarshipForm(
            instance=scholarship,
        )

    return render(
        request,
        "scholarships/scholarship_form.html",
        {
            "form": form,
            "scholarship": scholarship,
            "page_title": "Edit Scholarship",
            "submit_label": "Save Changes",
        },
    )


@login_required
def scholarship_delete(request, scholarship_id):
    """
    Delete a scholarship.
    """

    scholarship = get_object_or_404(
        Scholarship,
        id=scholarship_id,
    )

    if request.method == "POST":
        scholarship.delete()

        messages.success(
            request,
            "Scholarship deleted successfully.",
        )

        return redirect("scholarships:list")

    return render(
        request,
        "scholarships/scholarship_confirm_delete.html",
        {
            "scholarship": scholarship,
        },
    )