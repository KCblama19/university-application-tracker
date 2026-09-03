from django.urls import path

from . import views


app_name = "universities"


urlpatterns = [
    path("", views.university_list, name="list"),

    path(
        "add/",
        views.university_create,
        name="create",
    ),

    path(
        "<int:university_pk>/programs/add/",
        views.program_create,
        name="program-create",
    ),

    path(
        "programs/<int:pk>/edit/",
        views.program_update,
        name="program-update",
    ),

    path(
        "programs/<int:pk>/delete/",
        views.program_delete,
        name="program-delete",
    ),

    path(
        "<int:pk>/edit/",
        views.university_update,
        name="update",
    ),

    path(
        "<int:pk>/delete/",
        views.university_delete,
        name="delete",
    ),

    path(
        "<int:pk>/",
        views.university_detail,
        name="detail",
    ),
]