from django.urls import path

from . import views


app_name = "documents"


urlpatterns = [
    path("", views.document_list, name="list"),
    path("add/", views.document_create, name="create"),
    path("<int:document_id>/", views.document_detail, name="detail"),
    path(
        "<int:document_id>/edit/",
        views.document_update,
        name="update",
    ),
    path(
        "<int:document_id>/delete/",
        views.document_delete,
        name="delete",
    ),

    path(
        "applications/<int:application_id>/add/",
        views.application_document_create,
        name="application_document_create",
    ),

    path(
        "application-documents/<int:application_document_id>/edit/",
        views.application_document_update,
        name="application_document_update",
    ),

    path(
        "application-documents/<int:application_document_id>/delete/",
        views.application_document_delete,
        name="application_document_delete",
    ),
]