from django.contrib import admin

from .models import Scholarship


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "provider",
        "scholarship_type",
        "deadline",
        "stipend",
    )

    search_fields = (
        "name",
        "provider",
    )

    list_filter = (
        "scholarship_type",
        "deadline",
    )