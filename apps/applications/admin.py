from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "university",
        "program",
        "scholarship",
        "status",
        "application_deadline",
        "scholarship_deadline",
        "submitted_at",
    )

    search_fields = (
        "university__name",
        "program__name",
        "scholarship__name",
        "user__username",
        "user__email",
    )

    list_filter = (
        "status",
        "application_deadline",
        "scholarship_deadline",
    )

    date_hierarchy = "application_deadline"

    readonly_fields = (
        "created_at",
        "updated_at",
    )
