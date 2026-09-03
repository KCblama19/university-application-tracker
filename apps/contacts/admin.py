from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for university contacts.
    """

    list_display = (
        "name",
        "university",
        "position",
        "department",
        "email",
        "status",
        "last_contacted",
        "follow_up_date",
    )

    search_fields = (
        "name",
        "email",
        "university__name",
        "department",
        "research_area",
    )

    list_filter = (
        "status",
        "university",
        "follow_up_date",
    )

    date_hierarchy = "follow_up_date"

    readonly_fields = (
        "created_at",
        "updated_at",
    )