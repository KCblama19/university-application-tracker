from django.urls import path

from . import views


app_name = "contacts"


urlpatterns = [
    path("", views.contact_list, name="list"),
    path("add/", views.contact_create, name="create"),
    path(
        "applications/<int:application_id>/add/",
        views.contact_create,
        name="create_for_application",
    ),
    path(
        "<int:contact_id>/",
        views.contact_detail,
        name="detail",
    ),
    path(
        "<int:contact_id>/edit/",
        views.contact_update,
        name="update",
    ),
    path(
        "<int:contact_id>/delete/",
        views.contact_delete,
        name="delete",
    ),
]