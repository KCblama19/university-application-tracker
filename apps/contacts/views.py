from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .models import Contact


@login_required
def contact_list(request):
    """
    Display the user's contacts with optional status filtering.
    """

    contacts = (
        Contact.objects
        .filter(user=request.user)
        .select_related(
            "university",
            "application",
            "application__program",
        )
    )

    status = request.GET.get("status")

    if status:
        contacts = contacts.filter(status=status)

    return render(
        request,
        "contacts/contact_list.html",
        {
            "contacts": contacts,
            "status_choices": Contact.Status.choices,
            "current_status": status,
        },
    )


@login_required
def contact_create(request, application_id=None):
    """
    Create a new contact.

    When an application ID is provided, the contact is automatically
    associated with that application.
    """

    application = None

    if application_id is not None:
        from apps.applications.models import Application

        application = get_object_or_404(
            Application.objects.select_related("university"),
            id=application_id,
            user=request.user,
        )

    if request.method == "POST":
        form = ContactForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user

            if application is not None:
                contact.application = application
                contact.university = application.university

            contact.save()

            messages.success(
                request,
                "Contact created successfully.",
            )

            return redirect(
                "contacts:detail",
                contact_id=contact.id,
            )
    else:
        initial = {}

        if application is not None:
            initial["application"] = application
            initial["university"] = application.university

        form = ContactForm(
            user=request.user,
            initial=initial,
        )

    return render(
        request,
        "contacts/contact_form.html",
        {
            "form": form,
            "application": application,
            "page_title": "Add Contact",
            "submit_label": "Create Contact",
        },
    )


@login_required
def contact_detail(request, contact_id):
    """
    Display a single contact.
    """

    contact = get_object_or_404(
        Contact.objects.select_related(
            "university",
            "application",
            "application__program",
        ),
        id=contact_id,
        user=request.user,
    )

    return render(
        request,
        "contacts/contact_detail.html",
        {"contact": contact},
    )


@login_required
def contact_update(request, contact_id):
    """
    Update an existing contact.
    """

    contact = get_object_or_404(
        Contact,
        id=contact_id,
        user=request.user,
    )

    if request.method == "POST":
        form = ContactForm(
            request.POST,
            instance=contact,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Contact updated successfully.",
            )

            return redirect(
                "contacts:detail",
                contact_id=contact.id,
            )
    else:
        form = ContactForm(
            instance=contact,
            user=request.user,
        )

    return render(
        request,
        "contacts/contact_form.html",
        {
            "form": form,
            "contact": contact,
            "page_title": "Edit Contact",
            "submit_label": "Save Changes",
        },
    )


@login_required
def contact_delete(request, contact_id):
    """
    Delete a contact after confirmation.
    """

    contact = get_object_or_404(
        Contact,
        id=contact_id,
        user=request.user,
    )

    if request.method == "POST":
        contact.delete()

        messages.success(
            request,
            "Contact deleted successfully.",
        )

        return redirect("contacts:list")

    return render(
        request,
        "contacts/contact_confirm_delete.html",
        {"contact": contact},
    )