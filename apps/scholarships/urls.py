from django.urls import path

from . import views


app_name = "scholarships"


urlpatterns = [
    path(
        "",
        views.scholarship_list,
        name="list",
    ),
    path(
        "add/",
        views.scholarship_create,
        name="create",
    ),
    path(
        "<int:scholarship_id>/",
        views.scholarship_detail,
        name="detail",
    ),
    path(
        "<int:scholarship_id>/edit/",
        views.scholarship_update,
        name="update",
    ),
    path(
        "<int:scholarship_id>/delete/",
        views.scholarship_delete,
        name="delete",
    ),
]