from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.randomPage, name="random"),
    path("error-<int:errorType>", views.error, name="error"),
    path("search-error", views.search, name="search-error"),
    path("search", views.search, name="search"),
    path("new-entry", views.newEntry, name="new-entry"),
    path("edit", views.updateEntry, name="update-entry"),
    path("<str:subject>-edit", views.editEntry, name="edit-entry"),
    path("<str:subject>", views.entry, name="entry"),
]
