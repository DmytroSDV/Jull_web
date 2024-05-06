from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'notes'

urlpatterns = [
    path("users/profile/my_notes/", views.show_notes, name="notes_list"),
    path("users/profile/my_notes/add_notes", views.add_notes, name="add_notes"),
    path("users/profile/my_notes/delete_notes/<int:notes_id>/", views.delete_note, name="delete_notes"),
    path("users/profile/my_notes/edit_notes/<int:notes_id>/", views.edit_note, name="edit_notes"),
    path("users/profile/my_notes/search_note/", views.search_notes, name="search_notes"),
    path('users/profile/notes_by_tag/<str:tag>/', views.notes_by_tag, name='notes_by_tag'),
    path("users/profile/my_notes/<int:page>", views.show_notes, name="paginator_notes_list"),

]
