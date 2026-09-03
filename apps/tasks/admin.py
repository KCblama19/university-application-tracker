from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "application",
        "due_date",
        "priority",
        "status",
        "completed_at",
    )

    search_fields = (
        "title",
        "description",
        "application__university__name",
        "application__program__name",
        "user__username",
    )

    list_filter = (
        "status",
        "priority",
        "due_date",
    )

    date_hierarchy = "due_date"

    readonly_fields = (
        "created_at",
        "updated_at",
    )