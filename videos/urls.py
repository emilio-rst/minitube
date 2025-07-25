from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('upload/', views.upload_video, name='upload_video'),
    path('popular/', views.popular_videos, name='popular_videos'),
    path('history/', views.user_history, name='user_history'),
] 