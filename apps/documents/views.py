from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.applications.models import Application

from .forms import DocumentForm, ApplicationDocumentForm
from .models import Document, ApplicationDocument


@login_required
def document_list(request):
    """
    Display documents belonging to the currently logged-in user.
    """

    documents = Document.objects.filter(
        user=request.user
    )

    return render(
        request,
        "documents/document_list.html",
        {
            "documents": documents,
        },
    )


@login_required
def document_create(request):
    """
    Upload a new document to the user's document library.
    """

    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()

            messages.success(
                request,
                "Document uploaded successfully.",
            )

            return redirect("documents:list")
    else:
        form = DocumentForm()

    return render(
        request,
        "documents/document_form.html",
        {
            "form": form,
            "page_title": "Add Document",
            "submit_label": "Upload Document",
        },
    )


@login_required
def document_detail(request, document_id):
    """
    Display one document belonging to the current user.
    """

    document = get_object_or_404(
        Document,
        id=document_id,
        user=request.user,
    )

    return render(
        request,
        "documents/document_detail.html",
        {
            "document": document,
        },
    )


@login_required
def document_update(request, document_id):
    """
    Update a document in the user's document library.
    """

    document = get_object_or_404(
        Document,
        id=document_id,
        user=request.user,
    )

    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=document,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Document updated successfully.",
            )

            return redirect(
                "documents:detail",
                document_id=document.id,
            )
    else:
        form = DocumentForm(instance=document)

    return render(
        request,
        "documents/document_form.html",
        {
            "form": form,
            "document": document,
            "page_title": "Edit Document",
            "submit_label": "Save Changes",
        },
    )


@login_required
def document_delete(request, document_id):
    """
    Delete a document from the user's document library.
    """

    document = get_object_or_404(
        Document,
        id=document_id,
        user=request.user,
    )

    if request.method == "POST":
        document.delete()

        messages.success(
            request,
            "Document deleted successfully.",
        )

        return redirect("documents:list")

    return render(
        request,
        "documents/document_confirm_delete.html",
        {
            "document": document,
        },
    )
    

@login_required
def application_document_create(request, application_id):
    """
    Attach an existing document from the user's document library
    to a specific application.
    """

    application = get_object_or_404(
        Application,
        id=application_id,
        user=request.user,
    )

    if request.method == "POST":
        form = ApplicationDocumentForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            application_document = form.save(commit=False)
            application_document.application = application

            application_document.save()

            messages.success(
                request,
                "Document added to the application.",
            )

            return redirect(
                "applications:detail",
                application_id=application.id,
            )
    else:
        form = ApplicationDocumentForm(
            user=request.user,
        )

    return render(
        request,
        "documents/application_document_form.html",
        {
            "form": form,
            "application": application,
            "page_title": "Add Application Document",
            "submit_label": "Add Document",
        },
    )
    
@login_required
def application_document_update(
    request,
    application_document_id,
):
    """
    Update a document's requirements and submission status
    for a specific application.
    """

    application_document = get_object_or_404(
        ApplicationDocument.objects.select_related(
            "application",
            "document",
        ),
        id=application_document_id,
        application__user=request.user,
    )

    application = application_document.application

    if request.method == "POST":
        form = ApplicationDocumentForm(
            request.POST,
            instance=application_document,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Application document updated successfully.",
            )

            return redirect(
                "applications:detail",
                application_id=application.id,
            )
    else:
        form = ApplicationDocumentForm(
            instance=application_document,
            user=request.user,
        )

    return render(
        request,
        "documents/application_document_form.html",
        {
            "form": form,
            "application": application,
            "application_document": application_document,
            "page_title": "Edit Application Document",
            "submit_label": "Save Changes",
        },
    )
    
@login_required
def application_document_delete(
    request,
    application_document_id,
):
    """
    Remove a document from an application.

    This does not delete the actual document from the user's
    document library.
    """

    application_document = get_object_or_404(
        ApplicationDocument.objects.select_related(
            "application",
            "document",
        ),
        id=application_document_id,
        application__user=request.user,
    )

    application = application_document.application

    if request.method == "POST":
        application_document.delete()

        messages.success(
            request,
            "Document removed from the application.",
        )

        return redirect(
            "applications:detail",
            application_id=application.id,
        )

    return render(
        request,
        "documents/application_document_confirm_delete.html",
        {
            "application_document": application_document,
            "application": application,
        },
    )