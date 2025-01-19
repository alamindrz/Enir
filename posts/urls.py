from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
  path("upload_video/", views.upload_video, name="upload_video"),
  
  path('short-videos/<int:pk>/delete/', views.delete_video, name='delete_video'),
  
  path("video_list/", views.video_list, name="video_list"),
]