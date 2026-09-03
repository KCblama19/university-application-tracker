from django.urls import path

from . import views


app_name = "applications"


urlpatterns = [
    path("", views.application_list, name="list"),
    path("add/", views.application_create, name="create"),
    path("<int:application_id>/", views.application_detail, name="detail"),
    path(
        "<int:application_id>/edit/",
        views.application_update,
        name="update",
    ),
    path(
        "<int:application_id>/delete/",
        views.application_delete,
        name="delete",
    ),
    path(
        "university/<int:university_id>/programs/",
        views.university_programs,
        name="university_programs",
    ),
]