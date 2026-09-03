from django.contrib import admin

from .models import University, Program


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "country",
        "ranking",
    )

    search_fields = (
        "name",
        "city",
        "country",
    )

    list_filter = (
        "country",
    )


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "university",
        "degree_type",
        "study_language",
        "duration",
        "tuition_fee",
    )

    search_fields = (
        "name",
        "university__name",
    )

    list_filter = (
        "degree_type",
        "study_language",
    )