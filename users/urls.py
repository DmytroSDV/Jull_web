from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.loginuser, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("contacts/", views.contact_list, name="contacts"),
    path("contact/create/", views.contact_create, name="contact_create"),
    path("contact/<int:pk>/edit/", views.contact_edit, name="contact_edit"),
    path("contact/<int:pk>/delete/", views.contact_delete, name="contact_delete"),
    path('upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),
    path('contacts/search/', views.contact_search, name='contact_search'),
    path('contacts/<int:pk>/delete/confirm/', views.contact_confirm_delete, name='contact_confirm_delete'),
    path('users/profile/add_avatar/', views.add_avatar, name='add_avatar_url'),
    path('users/profile/change-avatar/', views.choose_new_avatar, name='change_avatar_profile'),
    path("reset-password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path("reset-password/done/", PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name="password_reset_done"),
    path("reset-password/confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                          success_url="/users/reset-password/complete/"),
         name="password_reset_confirm"),
    path("reset-password/complete/",
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),

    path('users/profile/add_avatar/', views.add_avatar, name='add_avatar_url'),
    path("contacts/<int:page>", views.contact_list, name="paginator_contacts"),


]
