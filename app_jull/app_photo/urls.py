from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'app_photo'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('gallery/', views.show_images, name='gallery'),
    path('gallery/delete/<int:image_id>/', views.delete_image, name='remove_image'),
    path('gallery/edit/<int:image_id>/', views.edit_image, name='edit_image'),
    path('gallery/download/<int:image_id>/', views.download_image, name='download_image'),
    path('gallery/my_photo', views.show_all_photo, name='show_photo'),
    path('gallery/my_video', views.show_all_video, name='show_video'),
    path('gallery/another', views.show_all_another, name='show_another')
]
