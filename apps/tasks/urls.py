from django.urls import path

from . import views


app_name = "tasks"


urlpatterns = [
    path("", views.task_list, name="list"),
    path("add/", views.task_create, name="create"),
    path(
    "applications/<int:application_id>/add/",
    views.task_create,
    name="create_for_application",
    ),
    path("<int:task_id>/", views.task_detail, name="detail"),
    path("<int:task_id>/edit/", views.task_update, name="update"),
    path("<int:task_id>/delete/", views.task_delete, name="delete"),
]