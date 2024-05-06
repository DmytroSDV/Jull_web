from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'app_photo'

urlpatterns = [
    path('users/profile/gallery/upload/', views.upload, name='upload'),
    path('users/profile/gallery/', views.show_images, name='gallery'),
    path('users/profile/gallery/delete/<int:image_id>/', views.delete_image, name='remove_image'),
    path('users/profile/gallery/edit/<int:image_id>/', views.edit_image, name='edit_image'),
    path('users/profile/gallery/download/<int:image_id>/', views.download_image, name='download_image'),
    path('users/profile/gallery/my_photo', views.show_all_photo, name='show_photo'),
    path('users/profile/gallery/my_video', views.show_all_video, name='show_video'),
    path('users/profile/gallery/another', views.show_all_another, name='show_another'),
    path('users/profile/gallery/<int:page>', views.show_images, name='paginator_gallery'),
    path('users/profile/gallery/my_photo/<int:page>', views.show_all_photo, name='paginator_show_photo'),
    path('users/profile/gallery/my_video/<int:page>', views.show_all_video, name='paginator_show_video'),
    path('users/profile/gallery/another/<int:page>', views.show_all_another, name='paginator_show_another')
]
