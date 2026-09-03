from django.contrib import admin

from .models import Document, ApplicationDocument


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "document_type",
        "user",
        "issue_date",
        "expiry_date",
        "created_at",
    )

    search_fields = (
        "name",
        "user__username",
        "user__email",
    )

    list_filter = (
        "document_type",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "document",
        "document_type",
        "required",
        "status",
        "submitted_at",
    )

    search_fields = (
        "application__university__name",
        "application__program__name",
        "document__name",
    )

    list_filter = (
        "status",
        "required",
        "document_type",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )